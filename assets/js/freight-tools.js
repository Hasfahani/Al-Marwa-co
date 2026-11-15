(function () {
    'use strict';
    var tools = window.FreightTools;
    if (!tools) return;
    function formError(form, message) {
        var error = form.querySelector('.freight-tool-error');
        if (!error) {
            error = document.createElement('p'); error.className = 'freight-tool-error'; error.setAttribute('role', 'alert'); form.appendChild(error);
        }
        error.textContent = message;
    }
    document.querySelectorAll('[data-interactive]').forEach(function (field) { field.disabled = false; });
    var planner = document.getElementById('freight-planner-form');
    if (planner) {
        var direction = document.getElementById('planner-direction'), origin = document.getElementById('planner-origin'),
            other = document.getElementById('planner-other-origin'), destination = document.getElementById('planner-destination'),
            load = document.getElementById('planner-load'), plannerResult = document.getElementById('planner-result');
        function updateRoute() {
            var exporting = direction.value === 'export', otherOrigin = !exporting && origin.value === 'Other';
            document.getElementById('planner-origin-label').hidden = exporting;
            origin.disabled = exporting;
            document.getElementById('planner-other-label').hidden = !otherOrigin;
            other.disabled = !otherOrigin; other.required = otherOrigin;
            document.getElementById('planner-destination-label').hidden = !exporting;
            destination.disabled = !exporting; destination.required = exporting;
            plannerResult.hidden = true;
        }
        direction.addEventListener('change', updateRoute); origin.addEventListener('change', updateRoute);
        load.addEventListener('change', function () { plannerResult.hidden = true; });
        other.addEventListener('input', function () { plannerResult.hidden = true; });
        destination.addEventListener('input', function () { plannerResult.hidden = true; });
        planner.addEventListener('submit', function (event) {
            event.preventDefault();
            if (!planner.reportValidity()) return;
            var result;
            try { result = tools.recommend({ direction: direction.value, origin: origin.value === 'Other' ? other.value : origin.value, destination: destination.value, load: load.value }); }
            catch (error) { formError(planner, error.message); plannerResult.hidden = true; return; }
            formError(planner, '');
            document.getElementById('planner-result-title').textContent = result.title;
            document.getElementById('planner-result-description').textContent = result.description;
            document.getElementById('planner-result-scope').textContent = result.scope;
            document.getElementById('planner-quote-link').href = 'contact.html?' + new URLSearchParams({ shipment_type: result.mode, origin: result.origin, destination: result.destination });
            plannerResult.hidden = false;
        });
        updateRoute();
    }
    var calculator = document.getElementById('cargo-calculator-form');
    if (!calculator) return;
    var rows = document.getElementById('cargo-rows'), resultPanel = document.getElementById('cargo-result'), current = null;
    function refreshRows() {
        rows.querySelectorAll('.cargo-row').forEach(function (row, index) {
            row.querySelector('legend').textContent = 'Package type ' + (index + 1);
            row.querySelector('.remove-cargo-row').disabled = rows.children.length === 1;
        });
        resultPanel.hidden = true; current = null;
    }
    function addRow() {
        var fragment = document.getElementById('cargo-row-template').content.cloneNode(true);
        fragment.querySelector('.remove-cargo-row').addEventListener('click', function (event) {
            event.currentTarget.closest('.cargo-row').remove(); refreshRows();
        });
        rows.appendChild(fragment); refreshRows();
    }
    document.getElementById('add-cargo-row').addEventListener('click', addRow);
    rows.addEventListener('input', function () { resultPanel.hidden = true; current = null; });
    rows.addEventListener('change', function () { resultPanel.hidden = true; current = null; });
    calculator.addEventListener('submit', function (event) {
        event.preventDefault();
        if (!calculator.reportValidity()) return;
        var packages = Array.from(rows.querySelectorAll('.cargo-row')).map(function (row) {
            var data = {};
            ['length', 'width', 'height', 'unit', 'quantity', 'weight'].forEach(function (key) { data[key] = row.querySelector('[name="' + key + '"]').value; });
            return data;
        });
        try { current = tools.calculate(packages); }
        catch (error) { formError(calculator, error.message); resultPanel.hidden = true; return; }
        formError(calculator, '');
        document.getElementById('cargo-volume').textContent = tools.format(current.volume) + ' m³';
        document.getElementById('cargo-quantity').textContent = current.quantity;
        document.getElementById('cargo-weight').textContent = current.completeWeight ? tools.format(current.weight) + ' kg' : 'Incomplete: ' + tools.format(current.weight) + ' kg known';
        document.getElementById('cargo-summary').textContent = tools.brief(current);
        document.getElementById('cargo-transfer-status').textContent = '';
        resultPanel.hidden = false;
    });
    document.getElementById('download-cargo-brief').addEventListener('click', function () {
        if (!current) return;
        var url = URL.createObjectURL(new Blob([tools.brief(current)], { type: 'text/plain;charset=utf-8' })), anchor = document.createElement('a');
        anchor.href = url; anchor.download = 'al-marwa-cargo-brief.txt'; document.body.appendChild(anchor); anchor.click(); anchor.remove();
        window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    });
    document.getElementById('cargo-use-quote').addEventListener('click', function () {
        if (!current) return;
        var details = current.pieces.map(function (piece) { return piece.quantity + ' x ' + tools.format(piece.length) + ' x ' + tools.format(piece.width) + ' x ' + tools.format(piece.height) + ' ' + piece.unit; }).join('; ');
        if (details.length > 1900) {
            document.getElementById('cargo-transfer-status').textContent = 'This packing list is too long for the short form field. Download the complete brief, then contact our freight desk with the full packing details.';
            return;
        }
        try {
            window.sessionStorage.setItem('al-marwa-cargo-draft', JSON.stringify({ createdAt: Date.now(), load_details: details + '; total ' + tools.format(current.volume) + ' m3', estimated_weight: current.completeWeight ? tools.format(current.weight) + ' kg' : '' }));
            window.location.href = 'contact.html';
        } catch (error) {
            document.getElementById('cargo-transfer-status').textContent = 'Your browser could not transfer the draft. Download the brief above, then open the contact page and copy its details.';
        }
    });
    addRow();
})();
