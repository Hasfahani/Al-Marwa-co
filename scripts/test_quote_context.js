'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../assets/js/main.js'), 'utf8');
function run(search, draft, contact = true) {
    const fields = contact ? {
        'shipment-type': { options: ['', 'FCL', 'FTL', 'Large Cargo', 'LCL', 'Air Cargo', 'Not Sure'].map(value => ({value})), value: '' },
        origin: {value: ''}, destination: {value: ''}, load_details: {value: ''}, estimated_weight: {value: ''}
    } : {};
    const listeners = {}, dispatched = [], storage = new Map();
    if (draft !== undefined) storage.set('al-marwa-cargo-draft', typeof draft === 'string' ? draft : JSON.stringify(draft));
    const inert = {classList: {add() {}, remove() {}, contains() {return false;}}, addEventListener() {}, appendChild() {}, setAttribute() {}};
    const document = {body: inert, documentElement: {scrollTop: 0}, getElementById(id) {return fields[id] || null;}, querySelectorAll() {return [];}, querySelector(selector) {const key = /name="([^"]+)"/.exec(selector); return key ? fields[key[1]] : null;}, createElement() {return {...inert};}, addEventListener(type, callback) {listeners[type] = callback;}};
    const window = {location: {search, pathname: '/contact.html'}, dataLayer: [], addEventListener() {}, dispatchEvent(event) {dispatched.push(event);}, sessionStorage: {getItem(key) {return storage.get(key);}, removeItem(key) {storage.delete(key);}}};
    class CustomEvent {constructor(type, options) {this.type = type; this.detail = options.detail;}}
    vm.runInNewContext(source, {document, window, URLSearchParams, Event, CustomEvent, breakpoints() {}, browser: {name: 'other', mobile: false}});
    return {fields, listeners, window, dispatched, storage};
}
let result = run('?shipment_type=LCL&origin=China&destination=Lebanon');
assert.equal(result.fields['shipment-type'].value, 'LCL'); assert.equal(result.fields.origin.value, 'China'); assert.equal(result.fields.destination.value, 'Lebanon');
result = run('?shipment_type=FCL&origin=Lebanon&destination=United+Kingdom');
assert.equal(result.fields.destination.value, 'United Kingdom');
result = run('?shipment_type=unknown&origin=' + 'x'.repeat(121));
assert.equal(result.fields['shipment-type'].value, ''); assert.equal(result.fields.origin.value, '');
result = run('', {createdAt: Date.now(), load_details: '4 x 120 x 80 x 100 cm; total 3.84 m3', estimated_weight: '1000 kg'});
assert.match(result.fields.load_details.value, /3.84/); assert.equal(result.fields.estimated_weight.value, '1000 kg'); assert.equal(result.storage.size, 0);
for (const draft of [{createdAt: Date.now() - 31 * 60 * 1000, load_details: 'expired'}, '{bad json']) {
    result = run('', draft); assert.equal(result.fields.load_details.value, ''); assert.equal(result.storage.size, 0);
}
assert.doesNotThrow(() => run('?shipment_type=FCL', undefined, false));
result = run('?shipment_type=FCL');
result.listeners.click({target: {closest() {return {getAttribute() {return 'https://wa.me/96170099978?text=example';}};}}});
assert.equal(result.window.dataLayer[0].event, 'freight_contact_click'); assert.equal(result.window.dataLayer[0].contact_method, 'whatsapp');
result.listeners.submit({target: {getAttribute() {return 'https://formsubmit.co/info@al-marwaco.com';}, querySelector() {return {value: 'FCL'};}}});
assert.equal(result.window.dataLayer[1].event, 'freight_quote_submission_attempt');
assert.deepEqual(Object.keys(result.window.dataLayer[1]).sort(), ['contact_method', 'event', 'page_path', 'shipment_type']);
console.log('Quote context checks passed: route parameters, temporary cargo drafts, expiry and non-personal measurement events.');
