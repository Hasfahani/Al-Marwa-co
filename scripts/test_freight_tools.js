'use strict';
const assert = require('node:assert/strict');
const tools = require('../assets/js/freight-tools-core.js');
function close(actual, expected) { assert.ok(Math.abs(actual - expected) < 1e-9, `${actual} != ${expected}`); }
let cargo = tools.calculate([{ length: 120, width: 80, height: 100, unit: 'cm', quantity: 4, weight: 250 }]);
close(cargo.volume, 3.84); assert.equal(cargo.quantity, 4); assert.equal(cargo.weight, 1000); assert.equal(cargo.completeWeight, true);
const equivalent = tools.calculate([{ length: 1.2, width: 0.8, height: 1, unit: 'm', quantity: 4, weight: 250 }]);
close(cargo.volume, equivalent.volume);
cargo = tools.calculate([{ length: 1000, width: 1000, height: 1000, unit: 'mm', quantity: 1, weight: '' }, { length: 1, width: 1, height: 1, unit: 'm', quantity: 2, weight: 300 }]);
close(cargo.volume, 3); assert.equal(cargo.quantity, 3); assert.equal(cargo.weight, 600); assert.equal(cargo.completeWeight, false);
assert.match(tools.brief(cargo), /incomplete/);
close(tools.calculate([{length: 10, width:10, height:10, unit:'in', quantity:1}]).volume, 0.016387064);
for (const bad of [[], [{length:-1,width:1,height:1,unit:'m',quantity:1}], [{length:1,width:1,height:1,unit:'m',quantity:1.5}], [{length:1,width:1,height:1,unit:'toString',quantity:1}], [{length:1,width:1,height:1,unit:'m',quantity:1,weight:-2}]]) assert.throws(() => tools.calculate(bad));
assert.notEqual(tools.format(1e-12), '0');
for (const origin of ['China','Turkey','United Arab Emirates','Jordan','Iraq','United Kingdom','Ukraine','UAE','uk','china']) {
    assert.equal(tools.recommend({direction:'import',origin,load:'smaller'}).mode,'LCL');
}
for (const origin of ['Australia','Germany','India','constructor']) {
    assert.equal(tools.recommend({direction:'import',origin,load:'smaller'}).mode,'FCL');
}
assert.equal(tools.recommend({direction:'export',destination:'China',load:'smaller'}).mode,'FCL');
assert.equal(tools.recommend({direction:'export',destination:'Australia',load:'large'}).mode,'Large Cargo');
assert.equal(tools.recommend({direction:'import',origin:'China',load:'truck'}).mode,'FTL');
assert.equal(tools.recommend({direction:'import',origin:'uae',load:'truck'}).mode,'FTL');
assert.equal(tools.recommend({direction:'export',destination:'Jordan',load:'truck'}).mode,'FTL');
assert.equal(tools.recommend({direction:'import',origin:'Australia',load:'truck'}).mode,'FCL');
assert.match(tools.recommend({direction:'import',origin:'Australia',load:'truck'}).description,/outside our core truckload lanes/);
assert.throws(() => tools.recommend({direction:'import',origin:' ',load:'container'}));
console.log('Freight tool checks passed: volume units, quantities, weights, invalid inputs, LCL origin scope and export scope.');
