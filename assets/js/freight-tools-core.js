(function (root, factory) {
    if (typeof module === 'object' && module.exports) module.exports = factory();
    else root.FreightTools = factory();
})(typeof window !== 'undefined' ? window : globalThis, function () {
    'use strict';
    var lclOrigins = ['China', 'Turkey', 'United Arab Emirates', 'Jordan', 'Iraq', 'United Kingdom', 'Ukraine'];
    function recommend(input) {
        if (!input || !['import', 'export'].includes(input.direction) || !['container', 'truck', 'large', 'smaller'].includes(input.load)) {
            throw new Error('Choose a shipment direction and load requirement.');
        }
        var origin = input.direction === 'export' ? 'Lebanon' : String(input.origin || '').trim();
        var alias = { uae: 'United Arab Emirates', uk: 'United Kingdom', 'u.k.': 'United Kingdom' };
        origin = (Object.prototype.hasOwnProperty.call(alias, origin.toLowerCase()) ? alias[origin.toLowerCase()] : null) || lclOrigins.find(function (country) { return country.toLowerCase() === origin.toLowerCase(); }) || origin;
        var destination = input.direction === 'export' ? String(input.destination || '').trim() : 'Lebanon';
        if (!origin || !destination || origin.length > 100 || destination.length > 100) throw new Error('Provide the origin and destination countries.');
        var result = { mode: 'FCL', origin: origin, destination: destination, title: 'Review a full-container shipment (FCL)', description: 'Worldwide FCL is our specialty for substantial business loads. Send the packed cargo details for a container and loading review.' };
        if (input.load === 'truck') {
            var lane = input.direction === 'export' ? (lclOrigins.find(function (country) { return country.toLowerCase() === destination.toLowerCase(); }) || (alias[destination.toLowerCase()] || null)) : (lclOrigins.includes(origin) ? origin : null);
            if (lane) {
                result.mode = 'FTL'; result.title = 'Request a full-truckload quote';
                result.description = 'We run full truckloads between ' + lane + ' and Lebanon. Send the pickup and delivery sites, packed load and readiness date, and the freight desk plans the vehicle, loading and routing.';
            } else {
                result.title = 'Review FCL for this route';
                result.description = (input.direction === 'export' ? destination : origin) + ' is outside our core truckload lanes (Ukraine, Jordan, Iraq, UAE, Turkey, UK, China). FCL, our worldwide specialty, is usually the better fit for a full business load on this route.';
            }
        } else if (input.load === 'large') {
            result.mode = 'Large Cargo'; result.title = 'Request a machinery or large-cargo review';
            result.description = 'Send transport dimensions, gross weight, photographs and loading requirements. We assess FCL or full-load handling according to cargo fit, sites and available routing.';
        } else if (input.load === 'smaller' && input.direction === 'import' && lclOrigins.includes(origin)) {
            result.mode = 'LCL'; result.title = 'Compare selected-route LCL with FCL';
            result.description = origin + ' is one of our selected LCL import origins into Lebanon. Acceptance, collection, consolidation, handling and route availability are confirmed for the shipment.';
        } else if (input.load === 'smaller') {
            result.description = 'This request is outside our published LCL scope. We can review an FCL arrangement for a business load. Compare the complete cargo and handling requirements before committing.';
        }
        result.scope = 'Planning guidance only. This is not a price, cargo acceptance, equipment reservation or confirmed route.';
        return result;
    }
    function calculate(rows) {
        if (!Array.isArray(rows) || !rows.length) throw new Error('Add at least one package type.');
        var factors = { m: 1, cm: 0.01, mm: 0.001, in: 0.0254 };
        var volume = 0, quantity = 0, weight = 0, completeWeight = true;
        var pieces = rows.map(function (row) {
            var length = Number(row.length), width = Number(row.width), height = Number(row.height), count = Number(row.quantity), factor = factors[row.unit];
            if (![length, width, height].every(function (n) { return Number.isFinite(n) && n > 0; }) || !Number.isInteger(count) || count < 1 || count > 10000 || typeof factor !== 'number') throw new Error('Provide positive dimensions, a valid unit, and a whole quantity from 1 to 10,000.');
            var grossWeight = row.weight === '' || row.weight === null || row.weight === undefined ? null : Number(row.weight);
            if (grossWeight !== null && (!Number.isFinite(grossWeight) || grossWeight < 0)) throw new Error('Gross weights must be zero or positive numbers.');
            var cubicMetres = length * factor * width * factor * height * factor * count;
            if (!Number.isFinite(cubicMetres)) throw new Error('The dimensions are too large to calculate.');
            volume += cubicMetres; quantity += count;
            if (grossWeight === null) completeWeight = false; else weight += grossWeight * count;
            return { length: length, width: width, height: height, unit: row.unit, quantity: count, weight: grossWeight, volume: cubicMetres };
        });
        if (!Number.isFinite(volume) || !Number.isFinite(weight)) throw new Error('The totals are too large to calculate.');
        return { volume: volume, quantity: quantity, weight: weight, completeWeight: completeWeight, pieces: pieces };
    }
    function format(number) { return number > 0 && number < 0.000001 ? number.toExponential(3) : new Intl.NumberFormat('en', { maximumFractionDigits: 6 }).format(number); }
    function brief(result) {
        var lines = ['AL MARWA CO - B2B cargo measurement brief', ''];
        result.pieces.forEach(function (piece, index) {
            lines.push('Package type ' + (index + 1) + ': ' + piece.quantity + ' x ' + format(piece.length) + ' x ' + format(piece.width) + ' x ' + format(piece.height) + ' ' + piece.unit + (piece.weight === null ? '; weight not supplied' : '; ' + format(piece.weight) + ' kg gross per piece'));
        });
        lines.push('', 'Total volume: ' + format(result.volume) + ' m3', 'Total packages: ' + result.quantity,
            (result.completeWeight ? 'Total gross weight: ' : 'Known gross weight (incomplete): ') + format(result.weight) + ' kg', '',
            'Packed measurements only. Container fit, load arrangement, cargo acceptance, route and price require review.',
            'Company: ', 'Origin / destination: ', 'Readiness date: ', 'Loading / delivery scope: ');
        return lines.join('\n');
    }
    return { recommend: recommend, calculate: calculate, brief: brief, format: format };
});
