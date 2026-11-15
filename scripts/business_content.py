"""Customer-focused business pages and practical freight planning resources."""


def section(title, paragraphs=(), bullets=(), html=''):
    return {'title':title,'paragraphs':list(paragraphs),'bullets':list(bullets),'html':html}


INDUSTRIES = [
    {
        'slug':'commercial-imports-lebanon.html','short_name':'Importers & Wholesalers',
        'title':'Freight for Lebanon Importers & Wholesalers | AL MARWA CO',
        'description':'B2B freight for Lebanese importers, wholesalers and distributors: worldwide FCL, commercial stock planning and selected-origin LCL imports into Lebanon.',
        'heading':'Freight for Importers, Wholesalers & Distributors',
        'eyebrow':'B2B · Commercial stock · Container loads','shipment':'FCL',
        'summary':'Purchase orders, stock replenishment and commercial container loads.',
        'audience':'Importers, wholesalers, distributors and trading companies',
        'parent':('freight-forwarding-lebanon.html','For Businesses'),
        'sections':[
            section('Turn purchase orders into a shipment plan',[
                'A purchase order describes what you bought. A useful freight brief also explains where each item is stored, when it will be ready, how it is packed, and who can release it. For full-container imports, these details let us review the loading requirement before a container or collection arrangement is confirmed.',
                'AL MARWA CO focuses on businesses moving substantial commercial loads to Lebanon. FCL worldwide is our specialty. We also review full truckloads on our seven core lanes and LCL imports from Ukraine, Jordan, Iraq, the UAE, Turkey, the United Kingdom, and China into Lebanon.',
            ]),
            section('Plan replenishment around the receiving warehouse',[
                'Tell us whether one order replenishes several stock lines or supports a single delivery commitment. Include the release date for the complete load, not only the date production starts. If different suppliers will release goods at different times, list those dates separately.',
                'At the Lebanese receiving end, provide unloading access, the warehouse contact, appointment needs, and any limits on vehicle or container access. An offer can then describe the pickup, freight, documentation coordination, and delivery tasks your business actually needs.',
            ]),
            section('What a recurring import brief should contain',bullets=[
                'Supplier addresses, packing lists and the party authorizing each collection.',
                'Expected container or truck count per order and the likely shipment frequency.',
                'Packed dimensions, gross weights, stacking limits and mixed-product loading needs.',
                'Readiness windows, receiving appointments and any stock availability deadlines.',
                'The agreed commercial handoff and which services should be included in each quote.',
            ]),
            section('Compare repeat orders on the same basis',[
                'Separate the goods cost from the freight scope. Ask whether a proposal includes collection, loading coordination, origin handling, the main freight leg, destination handling, and final delivery where requested. Comparing only one freight line can hide differences in what remains for your team to arrange.',
                'For a smaller order from a selected origin, compare LCL with FCL using the same collection and delivery points. Packaging and shared-container handling matter as well as cubic volume. The route and acceptance are confirmed for each actual shipment.',
            ]),
        ],
        'faqs':[
            ('Do you work with wholesalers and trading companies?', 'Yes. Our B2B focus includes importers, wholesalers, distributors and trading companies moving full containers, full truckloads on our seven core lanes, and substantial commercial loads.'),
            ('Can you review a recurring container import requirement?', 'Yes. Share the origin, goods profile, expected container count, shipment frequency, readiness pattern and receiving requirements. We define the operating scope around the actual lane and cargo.'),
            ('Can smaller wholesale orders use LCL?', 'We offer LCL imports into Lebanon only from Ukraine, Jordan, Iraq, the UAE, Turkey, the United Kingdom and China. Cargo acceptance, collection arrangements and route availability are confirmed individually.'),
            ('What helps avoid an incomplete import quote?', 'Provide the supplier and receiving addresses, itemized packing data, dates, loading and unloading responsibilities, and the pickup-to-delivery tasks you want included.'),
        ],
    },
    {
        'slug':'industrial-logistics-lebanon.html','short_name':'Manufacturers & Industry',
        'title':'Industrial Freight Lebanon | Manufacturers & Machinery | AL MARWA CO',
        'description':'B2B freight for manufacturers in Lebanon: full-container inputs, production equipment, industrial machinery and full-load delivery planning for business teams.',
        'heading':'Industrial Freight for Manufacturers & Production Teams',
        'eyebrow':'B2B · Manufacturing · Industrial equipment','shipment':'FCL',
        'summary':'Production inputs, factory equipment and installation handoffs.',
        'audience':'Manufacturers, industrial procurement teams and production operators',
        'parent':('freight-forwarding-lebanon.html','For Businesses'),
        'intro':'Production inputs, machinery purchases, and factory moves have different handling needs. AL MARWA CO plans FCL worldwide, substantial industrial loads, and full truckloads on our seven core lanes for manufacturers in Lebanon, with cargo readiness, loading requirements, and receiving access defined before booking.',
        'sections':[
            section('Separate production stock from equipment handling',[
                'Raw materials, packaged components, and a production machine should not be described as one undifferentiated order. Provide a packing list for the stock and individual transport details for equipment. Identify packages that cannot be stacked and units requiring a specific lifting or loading method.',
                'For recurring full-container inputs, share expected shipment frequency and the receiving arrangement at the plant. For machinery, include transport-state dimensions, gross weight, photographs and a clear explanation of who prepares the machine for collection.',
            ]),
            section('Connect the freight schedule with the factory handoff',[
                'If an installation team or production milestone depends on arrival, explain that requirement early. Distinguish the preferred arrival window from a confirmed site appointment. We review the freight option and handling scope against those needs without publishing a guaranteed transit time.',
                'Factory access also matters. Send vehicle clearances, loading bay details, the unloading equipment available and the contact responsible for acceptance. If lifting or final placement is needed, ask for that scope explicitly rather than assume it is included in transport.',
            ]),
            section('Industrial cargo information to prepare',bullets=[
                'Itemized commercial goods description and separate machinery packing details.',
                'Dimensions and gross weight in transport condition, including bases and crates.',
                'Lift points, permitted orientation, stacking limits and known handling restrictions.',
                'Origin release contact, plant receiving contact and readiness dates.',
                'Container or truck requirement, project milestones and requested site-handling tasks.',
            ]),
            section('Use urgent air cargo when the commercial need justifies it',[
                'Some production-critical components need an air cargo review. Share the actual deadline, dimensions and weight so we can assess the urgent commercial requirement separately. Air cargo is a supporting service; our primary focus remains FCL, full truckloads, machinery and large business loads.',
                'LCL imports are available only from our seven selected origins into Lebanon. For substantial industrial purchases from other countries, ask for an FCL assessment and include the complete handling requirement.',
            ]),
        ],
        'faqs':[
            ('Can you plan full-container imports for a manufacturer?', 'Yes. Send the supplier location, goods profile, packed dimensions, weight, expected container count and receiving arrangement. FCL worldwide is our main specialty.'),
            ('What does a machinery freight review need?', 'Provide transport dimensions, gross weight, packaging, lift points, photographs, pickup access and unloading requirements. Identify any dismantling or preparation still to be completed.'),
            ('Can a proposal include lifting or factory-site handling?', 'Tell us the tasks required and provide site access details. We review equipment and handling feasibility and define which tasks can be included in the agreed scope.'),
            ('Can you review an urgent production component?', 'Yes. Air cargo can be reviewed for urgent commercial requirements when timing justifies the cost. Acceptance and timing depend on the actual goods and route.'),
        ],
    },
    {
        'slug':'project-cargo-lebanon.html','short_name':'Project & Construction Teams',
        'title':'Project Cargo Lebanon | Large Equipment & B2B Freight | AL MARWA CO',
        'description':'Project cargo planning in Lebanon for machinery, bulky equipment and commercial loads. FCL, truckload reviews, lifting scope and site delivery coordination.',
        'heading':'Project Cargo for Construction & Equipment Teams',
        'eyebrow':'B2B · Project loads · Site coordination','shipment':'Large Cargo',
        'summary':'Large equipment, phased delivery and project-site access.',
        'audience':'Construction teams, project operators and equipment procurement teams',
        'parent':('freight-forwarding-lebanon.html','For Businesses'),
        'intro':'A large equipment movement involves the cargo, the loading method, the available route, and a receiving site that can accept it. AL MARWA CO reviews FCL and full-load requirements for project teams in Lebanon, with handling tasks and delivery responsibilities made explicit before the shipment is booked.',
        'sections':[
            section('Build the project brief by transportable piece',[
                'List every unit as it will travel. A working machine, a dismantled assembly, and a crated component have different dimensions and lifting requirements. Provide an itemized schedule with photographs, gross weights and the intended packaging for each transportable piece.',
                'Explain which pieces must travel together and which may be released in phases. If a supplier has not finished preparing an item for transport, distinguish current dimensions from the planned transport dimensions. This helps prevent the freight review from relying on a configuration that will change before loading.',
            ]),
            section('Define the delivery point inside the project scope',[
                'A site address does not by itself define unloading or placement. Tell us whether delivery ends at an accessible gate, a laydown area, or another receiving point. Provide access limits, vehicle clearances, working windows and the party supplying unloading equipment.',
                'If crane work, lifting or placement support is requested, include the site conditions and handling information needed for review. The offer should identify the agreed tasks and the responsibilities that remain with your project team.',
            ]),
            section('Project cargo review checklist',bullets=[
                'Transportable-piece list, drawings, photographs and gross weights.',
                'Cargo readiness by phase and any installation or receiving milestones.',
                'Loading and lifting points, transport orientation and securing requirements.',
                'Pickup and receiving-site access, clearances and working windows.',
                'Requested FCL, full truckload, lifting and delivery scope, with responsible contacts.',
            ]),
            section('Check the handling plan before committing the dispatch',[
                'FCL is our worldwide specialty. We review whether dedicated container use fits the actual cargo and loading needs. Full truckloads run on our seven core lanes. Oversized pieces get a dedicated feasibility review covering vehicle, container type, lifting and route.',
                'For a large item from an origin outside our main import markets, send the details for an FCL assessment. Our selected-origin LCL service is intended for commercial imports into Lebanon from the seven named markets, rather than a general solution for large one-off items worldwide.',
            ]),
        ],
        'faqs':[
            ('What is included in project cargo planning?', 'The review can cover transport dimensions, packaging, route feasibility, loading and lifting requirements, shipment phases and receiving-site access. The accepted quote defines the actual service scope.'),
            ('Can delivery be planned in several phases?', 'Share the release date and receiving requirement for each phase. We review the proposed sequence, cargo grouping and available freight options before confirming the plan.'),
            ('Do you guarantee transport for any oversized load?', 'No. We assess feasibility using the actual dimensions, weights, handling needs, sites, route and equipment availability. A proposed arrangement is confirmed for the individual shipment.'),
            ('How do we request an equipment project quote?', 'Send your company, route, transportable-piece list, photographs, readiness dates, project milestones and the requested lifting, loading and delivery tasks.'),
        ],
    },
]
INDUSTRIES[0]['intro']='AL MARWA CO works with importers, wholesalers, distributors, and trading companies moving commercial stock into Lebanon. Our core offer is FCL worldwide and substantial business loads, with full truckloads on our seven core lanes and selected-origin LCL imports for smaller commercial orders.'


RESOURCE_SECTIONS=[
    section('Start with a useful planning task', [
        'Use the freight planner to identify which published service should be reviewed for your route and load. Use the cargo volume calculator to calculate packed cubic volume and prepare a shipment brief. These tools help you organize a quote request; they do not check live carrier availability, calculate a freight price, or approve cargo for transport.',
    ],html='''<div class="freight-route-grid"><a class="freight-route-link" href="freight-planner-lebanon.html"><h3>Find the service to review ↗</h3><p>Match import or export direction and shipment scale to FCL, FTL, large cargo or selected-origin LCL.</p></a><a class="freight-route-link" href="cargo-volume-calculator.html"><h3>Calculate cargo volume ↗</h3><p>Calculate total CBM from package dimensions and prepare a load summary for your business quote.</p></a></div>'''),
    section('Make the quote scope easy to compare',[
        'A useful freight request defines the goods, loading unit, route and requested responsibilities. The cost guide explains why collection, handling and delivery scope affect a comparison. The Beirut planning guide covers shipment information and the main freight handoffs.',
    ],html='''<ul><li><a href="container-shipping-costs-lebanon.html">Container shipping costs: what the quote should include</a></li><li><a href="beirut-freight-guide.html">B2B shipment planning through Beirut</a></li><li><a href="downloads/b2b-freight-quote-checklist.txt" download>Download the B2B quote checklist (.txt)</a></li><li><a href="heavy-equipment-shipping-lebanon.html">Machinery measurements and loading review</a></li></ul>'''),
    section('Keep the service scope clear',[
        'FCL worldwide is our specialty for commercial imports to Lebanon and exports from Lebanon. Full truckloads run on our seven core lanes. LCL is offered only from Ukraine, Jordan, Iraq, the UAE, Turkey, the United Kingdom and China into Lebanon, subject to shipment and route confirmation.',
        'A calculator result does not establish container fit or equipment selection. Door openings, gross weight, loading method, orientation and usable space must also be reviewed for the actual shipment. Send the complete packing list rather than only a total volume.',
    ]),
]

RESOURCES={
    'slug':'freight-resources-lebanon.html','short_name':'Planning Tools & Guides','kind':'collection',
    'title':'B2B Freight Planning Tools & Guides | Lebanon | AL MARWA CO',
    'description':'Plan business freight in Lebanon with a service planner, cargo volume calculator, container cost guide and downloadable B2B quote checklist for commercial loads.',
    'heading':'Freight Planning Tools & Guides for Your Business',
    'intro':'Prepare a clearer container, truckload, or large-cargo inquiry. Explore practical tools, route guides, loading information, and a downloadable quote checklist from the AL MARWA CO business freight desk in Khalde, Lebanon.',
    'eyebrow':'B2B resources · Planning tools · Quote preparation','summary':'Practical freight tools, service decisions and quote preparation.',
    'parent':None,'sections':RESOURCE_SECTIONS,
    'faqs':[
        ('Do the planning tools provide a freight price?', 'No. The planner identifies the service to review, and the calculator measures packed cargo volume. A freight quote needs the actual route, cargo, dates and requested service scope.'),
        ('Can we download a quote checklist?', 'Yes. The B2B quote checklist is available as a text download on this page. It covers company details, the route, cargo, loading units, readiness and requested responsibilities.'),
        ('Does a CBM total confirm that cargo fits a container?', 'No. Usable space, openings, orientation, gross weight, packaging and loading method must also be checked. Provide an itemized packing list for review.'),
    ],
}

PLANNER_HTML='''<form id="freight-planner-form" class="freight-tool-form"><fieldset disabled data-interactive><legend>Tell us about the business shipment</legend>
<div class="freight-tool-fields"><label>Direction<select id="planner-direction" required><option value="import">Import to Lebanon</option><option value="export">Export from Lebanon</option></select></label>
<label id="planner-origin-label">Origin country<select id="planner-origin" required><option value="">Choose origin</option><option>China</option><option>Turkey</option><option>United Arab Emirates</option><option>Jordan</option><option>Iraq</option><option>United Kingdom</option><option>Ukraine</option><option value="Other">Another country</option></select></label>
<label id="planner-other-label" hidden>Origin country name<input id="planner-other-origin" maxlength="100" disabled></label>
<label id="planner-destination-label" hidden>Destination country<input id="planner-destination" maxlength="100" disabled></label>
<label>Shipment requirement<select id="planner-load" required><option value="">Choose a load</option><option value="container">Full container requirement</option><option value="truck">Full truckload requirement</option><option value="large">Machinery or a large commercial item</option><option value="smaller">Smaller commercial load</option></select></label></div>
<button type="submit" class="button primary">Review my service options</button></fieldset></form>
<noscript><p>Use the service guidance below or <a href="contact.html">contact our business freight desk</a>. The interactive planner requires JavaScript.</p></noscript>
<section id="planner-result" class="freight-tool-result" aria-live="polite" hidden><h3 id="planner-result-title"></h3><p id="planner-result-description"></p><p id="planner-result-scope"></p><a id="planner-quote-link" class="button primary" href="contact.html">Request a B2B review</a></section>'''

PLANNER={
    'slug':'freight-planner-lebanon.html','short_name':'Business Freight Planner','kind':'tool',
    'title':'B2B Freight Planner | FCL, FTL & LCL Lebanon | AL MARWA CO',
    'description':'Find which business freight service to review for imports to Lebanon or exports worldwide: FCL, full truckloads, large cargo or selected-origin LCL imports.',
    'heading':'Find the Freight Service to Review for Your Business',
    'intro':'Choose your shipment direction, country, and load requirement. The planner matches your inquiry to our published B2B service scope. The freight desk then reviews cargo details, route availability, handling, and the requested pickup and delivery tasks.',
    'eyebrow':'Business freight planner · FCL first','summary':'Match the shipment direction and load to the service scope.',
    'parent':('freight-resources-lebanon.html','Planning Tools & Guides'),
    'sections':[
        section('Plan a commercial shipment',html=PLANNER_HTML),
        section('How the planner makes a recommendation',[
            'A full-container requirement is directed to an FCL review. A full-truckload requirement is directed to a road-route assessment, with availability confirmed before any truck movement. Machinery or a large commercial item is directed to a cargo and loading review.',
            'For smaller commercial imports, the planner checks whether the origin is in the seven selected LCL markets. Smaller loads from other origins, and worldwide exports from Lebanon, are directed to an FCL review. The planner does not treat worldwide FCL coverage as worldwide LCL coverage.',
        ]),
        section('What to send after choosing a service',bullets=[
            'Your company and the actual pickup and delivery locations.',
            'Goods description, package count, packed dimensions and gross weights.',
            'Container or truck requirement, readiness date and delivery constraints.',
            'Loading method and the pickup, handling and delivery scope you need.',
        ]),
    ],
    'faqs':[
        ('Does the planner confirm a booking or route?', 'No. It identifies the service to review using the published scope. Cargo acceptance, available routes, schedules, equipment and prices are confirmed by the freight desk for the actual shipment.'),
        ('Why is a small shipment from another country directed to FCL?', 'Our LCL offer is limited to the seven selected origins into Lebanon. For another origin, we can assess whether dedicated-container use is practical for the business shipment.'),
        ('Which routes does FTL cover?', 'We run full truckloads between Lebanon and Ukraine, Jordan, Iraq, the UAE, Turkey, the United Kingdom and China. For other countries, the planner points you to FCL, our worldwide specialty.'),
    ],
}

CALCULATOR_HTML='''<form id="cargo-calculator-form" class="freight-tool-form"><fieldset disabled data-interactive><legend>Measure the packed cargo</legend><p>Enter external package dimensions. Weight is gross weight per piece. Add a separate row for each package type.</p><div id="cargo-rows"></div><div class="freight-actions"><button type="button" id="add-cargo-row" class="button">Add package type</button><button type="submit" class="button primary">Calculate volume</button></div></fieldset></form>
<template id="cargo-row-template"><fieldset class="cargo-row"><legend>Package type</legend><div class="cargo-row-fields"><label>Length<input name="length" type="number" min="0.001" step="any" required inputmode="decimal"></label><label>Width<input name="width" type="number" min="0.001" step="any" required inputmode="decimal"></label><label>Height<input name="height" type="number" min="0.001" step="any" required inputmode="decimal"></label><label>Unit<select name="unit"><option value="cm">cm</option><option value="m">m</option><option value="mm">mm</option><option value="in">inches</option></select></label><label>Quantity<input name="quantity" type="number" min="1" max="10000" step="1" value="1" required inputmode="numeric"></label><label>kg per piece (optional)<input name="weight" type="number" min="0" step="any" inputmode="decimal"></label></div><button type="button" class="remove-cargo-row button small">Remove this package type</button></fieldset></template>
<noscript><p>The calculator requires JavaScript. You can still <a href="contact.html">send the dimensions to our freight desk</a> or use the calculation example below.</p></noscript>
<section id="cargo-result" class="freight-tool-result" aria-live="polite" hidden><h3>Your cargo measurement summary</h3><dl class="cargo-totals"><div><dt>Total volume</dt><dd id="cargo-volume"></dd></div><div><dt>Total packages</dt><dd id="cargo-quantity"></dd></div><div><dt>Gross weight</dt><dd id="cargo-weight"></dd></div></dl><p>Calculated volume is not a loading plan, container-fit check or freight price. The packing arrangement, openings, weight and handling still need review.</p><pre id="cargo-summary" tabindex="0"></pre><div class="freight-actions"><button type="button" id="download-cargo-brief" class="button">Download the brief (.txt)</button><button type="button" id="cargo-use-quote" class="button primary">Use these details in a B2B quote</button></div><p id="cargo-transfer-status" role="status"></p></section>'''

CALCULATOR={
    'slug':'cargo-volume-calculator.html','short_name':'Cargo Volume Calculator','kind':'tool',
    'title':'Cargo Volume Calculator | CBM for Business Freight | AL MARWA CO',
    'description':'Calculate packed cargo volume in cubic metres from cm, m, mm or inches. Prepare a commercial shipment brief for FCL, truckloads or selected-route LCL review.',
    'heading':'Calculate Cargo Volume & Prepare a Business Shipment Brief',
    'intro':'Calculate total packed cubic volume (CBM), package count, and gross weight when supplied. Use the result to prepare a freight inquiry for containers, truckloads, or commercial cargo. Measurements help the review; they do not confirm a container, loading arrangement, or price.',
    'eyebrow':'Cargo volume calculator · Quote preparation','summary':'Calculate packed CBM and download an itemized shipment brief.',
    'parent':('freight-resources-lebanon.html','Planning Tools & Guides'),
    'sections':[
        section('Cargo volume calculator',html=CALCULATOR_HTML),
        section('How cubic volume is calculated',[
            'For each rectangular package type, convert the external length, width and height to metres, multiply those three measurements, then multiply by the quantity. Add the package-type totals together. For centimetres, divide each dimension by 100 before multiplying.',
            'For example, four packed units measuring 120 × 80 × 100 cm have a total volume of 3.84 m³. If each weighs 250 kg gross, their total gross weight is 1,000 kg. This calculation describes those packages; it does not prove how they can be arranged inside a container.',
        ]),
        section('Volume is one part of the loading review',[
            'Measure crates, pallets, protective frames and protruding parts as they will travel. Irregular machinery may need a transport envelope that includes space which cannot be filled with another package. Provide photographs and explain orientation or stacking restrictions.',
            'Do not subtract empty spaces inside equipment from its external transport dimensions. Container openings, loading access, usable floor space, weight distribution and lifting arrangements require a separate operational review. Our specialty is FCL worldwide and large B2B loads; LCL is limited to the selected origins into Lebanon.',
        ]),
    ],
    'faqs':[
        ('What does CBM mean?', 'CBM means cubic metres, a measure of volume. For rectangular packed goods it is calculated from length in metres multiplied by width in metres, height in metres and quantity.'),
        ('Should we measure the goods or their packaging?', 'Use external dimensions in transport condition, including pallets, crates, frames and protruding parts. Send separate rows for different package sizes.'),
        ('Does the calculator estimate a freight price?', 'No. It measures packed volume and sums supplied gross weights. A freight price needs the route, cargo, dates, handling requirements and requested service scope.'),
        ('Are calculator details sent to AL MARWA CO automatically?', 'No. Calculations run in your browser. Choosing the quote transfer keeps a temporary draft in your browser and opens the contact form. Information is sent only when you submit an inquiry through the form or contact a service yourself.'),
    ],
}

COST_GUIDE={
    'slug':'container-shipping-costs-lebanon.html','short_name':'Container Quote Cost Guide','kind':'guide',
    'title':'Container Shipping Costs Lebanon | B2B Quote Guide | AL MARWA CO',
    'description':'Understand what an FCL shipping quote to or from Lebanon should cover: collection, container handling, main freight, destination tasks and commercial scope.',
    'heading':'What Should a Container Shipping Quote Include?',
    'intro':'A useful FCL quote tells your business which transport and handling tasks are included. This guide helps importers and exporters compare the same pickup-to-delivery scope. It does not publish a freight rate: prices depend on the actual cargo, route, readiness, equipment, and requested responsibilities.',
    'eyebrow':'B2B FCL quote guide · Cost scope','summary':'Compare container quotes by included tasks and responsibilities.',
    'parent':('freight-resources-lebanon.html','Planning Tools & Guides'),
    'sections':[
        section('Compare the same start and end points',[
            'A port-to-port freight figure and a collection-to-delivery offer cover different work. State the actual pickup location, intended handoff, receiving address, and services you want included. If commercial terms have already been agreed with the supplier or buyer, include them in the request so the quote can reflect that arrangement.',
            'Ask which costs are included, which are excluded, and which depend on a later shipment event or a third-party requirement. A comparison is more useful when the proposals describe the same load, dates, equipment and service scope.',
        ],html='''<div class="freight-table-wrap"><table><caption>Tasks to define in a commercial container quote</caption><thead><tr><th scope="col">Part of the shipment</th><th scope="col">Question to clarify</th></tr></thead><tbody><tr><th scope="row">Origin collection</th><td>Where does collection start, and who releases and loads the goods?</td></tr><tr><th scope="row">Container and handling</th><td>Which equipment, loading and origin handling tasks are included?</td></tr><tr><th scope="row">Main freight</th><td>What route and service are being quoted for the specified load?</td></tr><tr><th scope="row">Destination tasks</th><td>Which port, documentation and delivery arrangements are included?</td></tr><tr><th scope="row">Final receiving</th><td>Who provides unloading, site access and any additional lifting?</td></tr></tbody></table></div>'''),
        section('Why cargo details change the comparison',[
            'The number of containers is not the only input. Dimensions, gross weight, packaging, stacking restrictions and loading method can change the equipment and handling requirement. Machinery may need preparation or site handling that ordinary boxed stock does not.',
            'For a single bulky item from another origin, ask whether an FCL arrangement is practical and compare the full scope. Dedicated container use does not require every cubic metre to be occupied. Our published LCL offer is limited to seven selected origins into Lebanon.',
        ]),
        section('Prepare the details before requesting rates',bullets=[
            'Your company, actual pickup point and final receiving point.',
            'Cargo description, packed dimensions, weights and container requirement.',
            'Readiness date, required arrival window and any agreed shipment frequency.',
            'Loading, unloading, lifting, documentation and delivery tasks requested.',
            'Commercial handoff terms already agreed and responsibilities still to be decided.',
        ]),
        section('Check the assumptions before accepting an offer',[
            'Read the quoted scope, validity and stated conditions. Confirm that the goods will be ready in the described transport condition and that both sites can provide the agreed access and handling. Ask how a change in cargo, dates, equipment or site requirements would be reviewed.',
            'The freight desk confirms the proposed arrangement for the actual shipment. Customs outcomes, live carrier space, routing and final transit timing are not determined by this guide or by a calculator result.',
        ]),
    ],
    'faqs':[
        ('Can you publish a single FCL rate for every Lebanon shipment?', 'No. A useful quote needs the actual origin and destination, cargo, container requirement, readiness and requested service scope. This guide explains cost scope rather than offering a fixed rate.'),
        ('What is the difference between a freight rate and total shipment scope?', 'A freight rate may describe only one transport leg. The full scope can also involve collection, loading, handling, documentation coordination, destination tasks and delivery where requested.'),
        ('Is LCL always cheaper for a smaller business load?', 'No. Compare the complete collection, consolidation, handling and delivery scope for the same shipment. LCL is offered only from our selected origins into Lebanon.'),
        ('What should we send for an FCL cost review?', 'Send company details, pickup and delivery points, a packing list with dimensions and gross weights, container needs, readiness date and requested handling and delivery tasks.'),
    ],
}

ARABIC_FCL={
    'slug':'fcl-shipping-lebanon-ar.html','short_name':'شحن الحاويات للشركات','language':'ar','locale':'ar-LB',
    'title':'شحن حاويات كاملة FCL في لبنان للشركات | المروة',
    'description':'شحن للشركات في لبنان: نتخصص في الحاويات الكاملة FCL عالمياً والشاحنات الكاملة والمعدات الكبيرة، مع شحن جزئي LCL إلى لبنان من سبع دول محددة.',
    'heading':'شحن حاويات كاملة FCL للشركات في لبنان وإلى العالم',
    'intro':'نتخصص في شحن الشركات B2B: حاويات كاملة FCL إلى لبنان من مختلف الدول، ومن لبنان إلى وجهات حول العالم، وشاحنات كاملة FTL من أوكرانيا والأردن والعراق والإمارات وتركيا والمملكة المتحدة والصين، ومعدات وبضائع تجارية كبيرة الحجم. من مكتبنا على أوتوستراد خلدة، نراجع تفاصيل الحمولة والمسار والتحميل والتسليم قبل تأكيد خطة الشحن.',
    'eyebrow':'شحن للشركات منذ 1997 · حاويات كاملة · حمولات كبيرة',
    'summary':'معلومات بالعربية عن الحاويات الكاملة وخدمة الشحن الجزئي المحددة.',
    'parent':None,'shipment':'FCL',
    'sections':[
        section('للمستوردين والمصدرين والمصانع وتجار الجملة',[
            'نركز على الشركات التي تنقل مخزوناً تجارياً أو مواد ومعدات صناعية أو حمولات كبيرة تحتاج إلى حاويات كاملة أو شاحنات كاملة. تشمل المراجعة حجم الحمولة ووزنها وحالتها بعد التغليف، وموقع الاستلام الفعلي، وجهة التسليم، والموعد الذي تكون فيه البضاعة جاهزة.',
            'الحاوية المخصصة FCL لا تشترط ملء كل المساحة المتاحة. يمكن دراسة شحن آلة واحدة كبيرة ضمن حاوية مخصصة عندما تتناسب أبعادها ووزنها وطريقة تحميلها مع الحل المتاح. نراجع ملاءمة الحمولة وتكاليف النطاق المطلوب قبل تأكيد العرض.',
        ]),
        section('شحن جزئي LCL إلى لبنان من دول محددة فقط',[
            'تتوفر خدمة الشحن الجزئي LCL إلى لبنان من أوكرانيا والأردن والعراق والإمارات وتركيا والمملكة المتحدة والصين فقط، بعد مراجعة قبول البضاعة والمسار والتوفر لكل شحنة. هذه الخدمة لا تعني شحناً جزئياً عالمياً من كل الدول أو تصدير شحنات جزئية من لبنان إلى كل الوجهات.',
            'للبضائع الكبيرة من دول أخرى، يمكن إرسال التفاصيل لدراسة حل FCL. ونشغّل شاحنات كاملة FTL برّاً من الدول السبع إلى لبنان، مع تأكيد المسار ونوع الشاحنة والموعد لكل شحنة.',
        ]),
        section('المعلومات اللازمة لعرض سعر واضح',bullets=[
            'اسم الشركة ونشاطها وبيانات الشخص المسؤول عن الشحنة.',
            'موقع الاستلام والوجهة الفعلية وبيانات المورد والجهة المستلمة.',
            'وصف البضاعة وعدد القطع والأبعاد بعد التغليف والوزن الإجمالي.',
            'عدد الحاويات أو الشاحنات المطلوبة، أو قائمة تعبئة كاملة لتقييم الاحتياج.',
            'تاريخ الجاهزية والموعد المطلوب ومتطلبات التحميل والرفع والتفريغ.',
            'صور أو رسومات للمعدات الكبيرة وأي قيود على الوصول إلى الموقع.',
        ]),
        section('خطة الشحنة تشمل المسؤوليات المطلوبة',[
            'عند طلب العرض، حدد إن كنت تحتاج إلى الاستلام أو تنسيق التحميل أو النقل الرئيسي أو متابعة المستندات أو التسليم النهائي. نراجع المهام المطلوبة ونوضح النطاق الذي يمكن إدراجه في العرض، والمسؤوليات التي يتولاها المورد أو المستلم.',
            'تتوفر أدلة المسارات وأدوات حساب الحجم باللغة الإنجليزية أيضاً. حساب الحجم يساعد في تجهيز الطلب، لكنه لا يؤكد ملاءمة الحاوية أو التوفر أو سعر الشحن. يمكن التواصل مع فريقنا وإرسال تفاصيل الشحنة مباشرة عبر الهاتف أو البريد الإلكتروني أو واتساب.',
        ],html='''<div class="freight-actions"><a href="cargo-volume-calculator.html" class="button" hreflang="en-LB">حاسبة حجم البضائع (English)</a><a href="shipping-routes-lebanon.html" class="button" hreflang="en-LB">مسارات الاستيراد (English)</a></div>'''),
    ],
    'faqs':[
        ('ما تخصص شركة المروة في الشحن؟','نركز على شحن الشركات B2B: الحاويات الكاملة FCL عالمياً، والشاحنات الكاملة من دولنا السبع الرئيسية، والمعدات والحمولات التجارية الكبيرة، مع خدمة LCL إلى لبنان من سبع دول محددة.'),
        ('من أي دول تتوفر خدمة LCL إلى لبنان؟','تتوفر طلبات الشحن الجزئي إلى لبنان من أوكرانيا والأردن والعراق والإمارات وتركيا والمملكة المتحدة والصين فقط، بعد تأكيد قبول البضاعة والمسار والتوفر لكل شحنة.'),
        ('هل يمكن شحن آلة واحدة كبيرة من دولة أخرى؟','يمكن دراسة شحنها ضمن حاوية مخصصة FCL بعد مراجعة الأبعاد والوزن والتغليف وطريقة التحميل والمسار. لا يشترط أن تملأ البضاعة كامل مساحة الحاوية.'),
        ('هل تقدمون موعد وصول أو سعراً ثابتاً لكل الشحنات؟','لا. يحدد العرض بناءً على المسار والبضاعة والجاهزية والمعدات والخدمات المطلوبة. يتم تأكيد التوفر والتوقيت والنطاق لكل شحنة على حدة.'),
    ],
}

from routes_ar import ROUTES_AR
ARABIC_FCL['sections'].insert(2,section('مسارات الاستيراد إلى لبنان بالعربية',[
    'نشحن حاويات كاملة وشاحنات كاملة وشحنات جزئية إلى لبنان من سبع دول رئيسية. اختر بلد المنشأ لمعرفة التفاصيل التي نحتاجها لعرض سعر سريع ودقيق.',
],html='<div class="freight-route-grid">'+''.join(f'<a class="freight-route-link" href="{r["slug"]}"><h3>من {r["country"]} إلى لبنان</h3><p>{r["summary"]}</p></a>' for r in ROUTES_AR)+'</div>'))

BUSINESS_PAGES=INDUSTRIES+[RESOURCES,PLANNER,CALCULATOR,COST_GUIDE,ARABIC_FCL]
