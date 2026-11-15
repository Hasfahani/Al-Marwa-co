"""Build the static B2B service and route pages. No build step is needed to serve them.

Content lives here; shared header, footer and business identity come from the
existing sea-freight page. Run from any directory after editing these pages' copy.
"""
from __future__ import annotations

from copy import deepcopy
from html import escape
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode

sys.dont_write_bytecode = True
from site_navigation import header_markup

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://al-marwaco.com/'
ORIGINS = 'Ukraine, Jordan, Iraq, the UAE, Turkey, the United Kingdom, and China'
LCL_SCOPE = f'LCL imports are offered only from {ORIGINS} into Lebanon, subject to shipment acceptance and route confirmation.'


def quote_url(shipment='FCL', origin='', destination='Lebanon'):
    return 'contact.html?' + urlencode({'shipment_type': shipment, 'origin': origin, 'destination': destination})


def section(title, paragraphs=(), bullets=()):
    return {'title': title, 'paragraphs': list(paragraphs), 'bullets': list(bullets)}


ROUTES = [
    {
        'slug': 'china-to-lebanon-shipping.html', 'country': 'China',
        'title': 'China to Lebanon Shipping | B2B FCL & LCL | AL MARWA CO',
        'description': 'B2B shipping from China to Lebanon for full containers, machinery and wholesale goods. Selected-route LCL imports, loading review and commercial freight quotes.',
        'heading': 'China to Lebanon Shipping for Business Cargo',
        'intro': 'Importing factory orders, wholesale stock, or industrial equipment from China? AL MARWA CO plans FCL shipments into Lebanon around the actual supplier address, packed cargo, and receiving requirements. FCL is our specialty; LCL is also available on this selected import route after shipment review.',
        'summary': 'Factory orders, multiple suppliers and container loading plans.',
        'sections': [
            section('Build the plan around the supplier, not just the country', [
                'A China-to-Lebanon inquiry becomes more useful when it identifies where the goods will actually be collected. A factory address, a trading company address, and a storage location may describe different handoffs. Confirm which party can release the cargo and which loading tasks are included in the commercial sale.',
                'If several suppliers contribute to one order, provide a separate packing list and readiness date for each. We can then review the collection and loading scope before quoting. A single combined purchase value does not show how much space, handling, or coordination the shipment needs.',
            ]),
            section('China import checklist for full containers', bullets=[
                'Supplier collection addresses, contact people and cargo release dates.',
                'Packed dimensions and gross weight by carton, pallet or machine.',
                'Number of containers requested, or the complete packing list if undecided.',
                'Whether goods can be stacked and whether machinery needs special loading access.',
                'Lebanese consignee, unloading address and required pickup-to-delivery scope.',
            ]),
            section('Example planning brief: equipment and wholesale stock', [
                'For an order combining a machine with boxed stock, send the machine dimensions separately from the cartons. Photos of the packed machine, its base, and loading points help distinguish its handling needs from ordinary stock. Identify any parts shipped loose and any limits on stacking around the equipment.',
                'Container selection and the final loading arrangement are confirmed once the cargo details are in. For a smaller commercial order, ask for an LCL assessment that includes handling and destination charges as well as the freight leg.',
            ]),
        ],
        'faqs': [
            ('Can you ship a full container from China to Lebanon?', 'Yes. FCL is our main specialty. Send the supplier location, cargo description, packed dimensions, total weight, container requirement, and readiness date so we can review the shipment into Lebanon.'),
            ('Can one China order include goods from several suppliers?', 'Yes. Send each supplier address, packing list, and readiness date. We plan the collections and combined loading into one shipment where supplier timing allows.'),
            ('Do you offer LCL from China into Lebanon?', 'Yes. China is one of our selected LCL import origins into Lebanon. Cargo acceptance, collection scope, consolidation arrangements, and availability are confirmed for the shipment.'),
            ('What should a machinery supplier send before loading?', 'Ask for packed length, width, height, gross weight, loading and lifting points, packaging details, and photographs. These help us assess container fit and the handling scope before booking.'),
        ],
    },
    {
        'slug': 'turkey-to-lebanon-shipping.html', 'country': 'Turkey',
        'title': 'Turkey to Lebanon Shipping | B2B FCL & Full Loads | AL MARWA CO',
        'description': 'Commercial shipping from Turkey to Lebanon for FCL, full truckload assessments, machinery and wholesale cargo. Selected-route LCL imports for businesses.',
        'heading': 'Turkey to Lebanon Freight for Full Business Loads',
        'intro': 'Plan commercial imports from Turkey to Lebanon with a freight desk focused on full containers, full truckloads on our seven core lanes, and bulky goods. AL MARWA CO reviews pickup, loading, and delivery needs before proposing the route. Selected-route LCL imports into Lebanon are also available.',
        'summary': 'Factory pickup, pallet layouts, bulky goods and truckload review.',
        'sections': [
            section('Choose the load arrangement before choosing the vehicle', [
                'For a Turkish factory or warehouse order, the packed shipment matters more than the product catalogue dimensions. Furniture, assembled equipment, and irregular loads can occupy space that cannot be used by another pallet. Tell us which items may be stacked and which need to remain upright.',
                'Turkey is one of our main full-truckload lanes into Lebanon, with FCL as the alternative when sea freight suits the cargo better. Send the actual pickup and receiving addresses, loading access and the scope you need, and we plan the vehicle around the load.',
            ]),
            section('Details that help with factory and warehouse collections', bullets=[
                'Factory or warehouse address and a contact who can authorize release.',
                'Pallet count, packed dimensions, gross weight and stacking limits.',
                'Whether the supplier loads from a dock, forklift area or overhead lifting point.',
                'Loading appointment requirements and the date the full order will be ready.',
                'Delivery access in Lebanon, including whether unloading equipment is available.',
            ]),
            section('Example planning brief: bulky goods with limited stacking', [
                'For a wholesale furniture order or assembled production equipment, list the floor space each package needs and identify fragile surfaces. Provide photographs of the finished packaging. That allows the freight plan to account for the usable space around the goods and any loading restrictions.',
                'If your shipment is smaller, we can review LCL into Lebanon from Turkey. Compare the complete collection, handling, and delivery scope with the FCL option. For recurring orders, include expected frequency and the range of shipment sizes rather than treating every order as identical.',
            ]),
        ],
        'faqs': [
            ('Can you review a full truckload from Turkey to Lebanon?', 'Yes. Send the exact pickup and delivery addresses, packed cargo dimensions and weight, loading method, and readiness date. We plan the vehicle, routing and loading for your shipment and confirm them in the offer.'),
            ('Is FCL available for bulky goods from Turkey?', 'Yes. FCL is our specialty, including business cargo from Turkey into Lebanon. We review container fit, loading access, packaging, and the delivery scope for the actual shipment.'),
            ('How should we describe non-stackable cargo?', 'List the dimensions of every packed unit, its gross weight, required orientation, and any surfaces that cannot carry another item. Photographs help explain restrictions that a total volume figure may miss.'),
            ('Can a smaller commercial order use LCL from Turkey?', 'Turkey is one of our selected LCL origins into Lebanon. Send the packed cargo details for acceptance and route confirmation, including collection and final-delivery requirements.'),
        ],
    },
    {
        'slug': 'uae-to-lebanon-shipping.html', 'country': 'United Arab Emirates',
        'title': 'UAE to Lebanon Shipping | B2B FCL & Large Cargo | AL MARWA CO',
        'description': 'B2B shipping from the UAE to Lebanon for full containers, industrial equipment and warehouse stock. Selected-route LCL and full-load route assessments.',
        'heading': 'UAE to Lebanon Shipping for Commercial Loads',
        'intro': 'Moving warehouse stock, trading-company orders, or industrial equipment from the UAE to Lebanon? AL MARWA CO focuses on FCL and substantial business loads, with full truckloads by road on this lane. The UAE is also one of our selected origins for LCL imports into Lebanon.',
        'summary': 'Warehouse release, trading orders and equipment collection scope.',
        'sections': [
            section('Identify the stock location and the party releasing it', [
                'A supplier based in the UAE may arrange release from a different warehouse or storage site. Share the actual collection address, the warehouse contact, and the party responsible for authorizing release. If an order has more than one pickup point, identify the quantity at each location.',
                'For goods purchased through a trader, keep the goods description, seller, and collection point clear in the shipment brief. Tell us which documents are already available and which party is preparing the remaining paperwork. Document and route requirements are reviewed for the actual cargo; a UAE pickup does not establish the goods origin.',
            ]),
            section('Prepare a warehouse collection brief', bullets=[
                'Actual stock address, release contact and any collection reference.',
                'Whether all items are ready together or released in separate lots.',
                'Gross weights and packed dimensions, especially for equipment and tanks.',
                'Forklift, crane or loading-bay access at the collection location.',
                'Requested FCL, FTL or LCL scope and the unloading arrangements in Lebanon.',
            ]),
            section('Example planning brief: a machine held in storage', [
                'Before requesting collection of a stored machine, obtain current photographs and confirmation of its packed state. A machine advertised for sale may still need dismantling, securing, or a transport base. Identify who will carry out that work and who will make it ready for loading.',
                'We use the completed load details to review FCL fit, handling, and the agreed delivery scope. If you prefer road transport, we quote a full truckload from the UAE as well. A smaller commercial shipment can be considered for selected-route LCL into Lebanon after acceptance review.',
            ]),
        ],
        'faqs': [
            ('Do you collect UAE business cargo for FCL shipping to Lebanon?', 'We can review UAE-origin commercial cargo for an FCL plan into Lebanon. Provide the actual stock location, release contact, packing list, loading arrangements, and desired pickup and delivery scope.'),
            ('What if the UAE seller uses a separate warehouse?', 'Give both the seller contact and the actual warehouse release contact. Confirm who authorizes collection, when the stock is ready, and which pickup tasks need to be included in the quote.'),
            ('Can you assess equipment that is not yet packed?', 'Yes, for planning. Send its current dimensions, weight, photographs, and the intended transport packaging. Final acceptance and loading arrangements depend on the completed shipment profile.'),
            ('Does the UAE route include LCL and full truckloads?', 'The UAE is a selected LCL origin into Lebanon. Full truckloads by road are also part of this lane. Each service, scope, and schedule is confirmed for the specific shipment.'),
        ],
    },
    {
        'slug': 'jordan-to-lebanon-shipping.html', 'country': 'Jordan',
        'title': 'Jordan to Lebanon Freight | B2B Full Truckloads | AL MARWA CO',
        'description': 'B2B freight from Jordan to Lebanon for full truckloads on our seven core lanes, FCL and large commercial loads. Selected-route LCL import planning and quotes.',
        'heading': 'Jordan to Lebanon Freight for Business Shipments',
        'intro': 'AL MARWA CO reviews full truckloads, full-container requirements, and large commercial cargo from Jordan into Lebanon. We work with businesses that need a clear pickup and delivery scope, defined loading responsibilities, and a route confirmed before dispatch. Selected-route LCL imports are also available.',
        'summary': 'Full truckloads, receiving appointments and loading responsibility.',
        'sections': [
            section('Start a truckload inquiry with the two loading sites', [
                'For a Jordan-to-Lebanon business shipment, tell us where the goods will be loaded and where they will be unloaded. Include site access, vehicle restrictions, opening windows, and the equipment available at both ends. These details help establish whether the proposed truckload can be handled as requested.',
                'Full truckload planning is distinct from simply counting packages. The dimensions, weight distribution, and loading method affect the equipment needed. Route feasibility and availability must also be checked for the shipment. We confirm the operating scope before cargo is released for movement.',
            ]),
            section('What to include for a Jordan full-load quote', bullets=[
                'Shipper and consignee business details, with exact site addresses.',
                'Cargo dimensions, gross weight, pallet count and whether goods can be stacked.',
                'Required number of vehicles or containers, if already known.',
                'Loading and unloading equipment, appointment windows and site contacts.',
                'Readiness date, delivery target and agreed collection or delivery responsibilities.',
            ]),
            section('Example planning brief: a scheduled wholesale delivery', [
                'For a distributor sending a full commercial load to a Lebanese warehouse, match the stock release date with the receiving appointment. Identify who counts and checks the packages at collection, who loads them, and who has equipment ready to unload on arrival.',
                'If the order may be split across dates, explain the release quantities rather than quoting only an overall project total. We can review the proposed FTL or FCL requirement on that basis. Smaller business loads can be assessed for LCL into Lebanon because Jordan is one of our selected origins.',
            ]),
        ],
        'faqs': [
            ('Do you run full truckloads from Jordan to Lebanon?', 'Yes. Jordan is one of our core full-truckload lanes. Send the exact cargo and loading sites and we confirm the vehicle, route and quoted scope.'),
            ('What site details affect a Jordan truckload quote?', 'Send address and access details, loading-bay or crane requirements, working windows, vehicle restrictions, and the equipment available for loading and unloading.'),
            ('Can you assess a full-container requirement from Jordan?', 'Yes. Share the cargo profile and preferred service scope. FCL is our specialty worldwide; the practical routing and handling for a Jordan-origin shipment are assessed before booking.'),
            ('Is LCL from Jordan within your import coverage?', 'Yes. Jordan is one of our selected LCL origins into Lebanon. Shipment acceptance, routing, and the required collection and delivery scope are confirmed individually.'),
        ],
    },
    {
        'slug': 'iraq-to-lebanon-shipping.html', 'country': 'Iraq',
        'title': 'Iraq to Lebanon Freight | B2B FTL & Large Cargo | AL MARWA CO',
        'description': 'Commercial freight from Iraq to Lebanon for full truckload reviews, FCL and industrial cargo. Loading access, project requirements and selected-route LCL.',
        'heading': 'Iraq to Lebanon Freight for Large Commercial Loads',
        'intro': 'For businesses importing equipment, stock, or project cargo from Iraq into Lebanon, AL MARWA CO reviews the load, collection conditions, and route before quoting. Our focus is substantial B2B shipments: full truckloads on our seven core lanes, FCL requirements, and large cargo. Selected-route LCL imports are also available.',
        'summary': 'Project-site collection, industrial units and cargo release readiness.',
        'sections': [
            section('Separate cargo readiness from collection readiness', [
                'Equipment may be available for sale or transfer before a site can release it for transport. Identify the person authorizing release, where the cargo stands, and whether it can be reached by the required vehicle or lifting equipment. Provide the actual location rather than a business billing address.',
                'For an industrial unit, describe its transport condition: assembled, dismantled, crated, or secured to a base. If several pieces form one machine, list them separately and explain which must travel together. We review the pickup and loading requirements alongside the available route.',
            ]),
            section('Information for Iraq-origin industrial or project cargo', bullets=[
                'Collection-site address, access contact and release authorization arrangements.',
                'Dimensions and gross weight for each transportable piece.',
                'Photographs, lifting points and loading method for heavy equipment.',
                'Whether dismantling, packing or a transport base is still required.',
                'Receiving-site access in Lebanon and who provides unloading equipment.',
            ]),
            section('Example planning brief: equipment transferred between sites', [
                'For a company transferring machinery into Lebanon, start with an inventory of the units in their proposed transport state. Name the party responsible for preparing and securing each item. If loading needs a crane, provide site photographs and any known access limits so that handling is included in the review.',
                'The freight plan can then assess an FTL or FCL requirement rather than assuming one transport unit fits everything. For smaller commercial cargo, LCL is within our selected Iraq-to-Lebanon import coverage, subject to shipment and route confirmation.',
            ]),
        ],
        'faqs': [
            ('Can you review heavy equipment from Iraq into Lebanon?', 'Yes. Send the actual collection location, dimensions, weight, transport condition, photographs, and lifting requirements. The loading plan, route, and equipment availability are reviewed before acceptance.'),
            ('Do you run full truckloads from Iraq to Lebanon?', 'Yes. Iraq is one of our core full-truckload lanes into Lebanon. Send the collection and delivery sites and the cargo profile; the quote confirms vehicle, routing and timing for that shipment.'),
            ('Can several machine components be quoted together?', 'Yes. Provide an itemized packing list with separate weights and dimensions, plus any pieces that must travel together. This helps assess vehicle or container count and loading needs.'),
            ('Do you accept Iraq-origin LCL inquiries?', 'Iraq is one of our selected origins for LCL imports into Lebanon. Acceptance, routing, handling, and any collection or delivery requirements are confirmed for each inquiry.'),
        ],
    },
    {
        'slug': 'uk-to-lebanon-shipping.html', 'country': 'United Kingdom',
        'title': 'UK to Lebanon Shipping | B2B FCL & Machinery | AL MARWA CO',
        'description': 'B2B shipping from the United Kingdom to Lebanon for full containers, machinery and bulky commercial goods. Selected-route LCL imports and loading review.',
        'heading': 'UK to Lebanon Shipping for Containers & Machinery',
        'intro': 'AL MARWA CO plans business shipments from the United Kingdom to Lebanon, with FCL as the main offer for machinery, equipment, and substantial commercial loads. We review the collection address, transport packaging, and loading responsibilities before booking. The UK is also a selected origin for LCL imports into Lebanon.',
        'summary': 'Machinery purchases, seller handover and container fit.',
        'sections': [
            section('Check what the seller is handing over', [
                'When purchasing machinery or bulky commercial goods in the UK, establish whether the seller provides a packed, load-ready shipment or expects collection of the equipment in its current position. Confirm who dismantles, packs, lifts, and loads it. Those tasks change the collection scope and the information needed for a quote.',
                'Use packed dimensions for the final transport plan. If the equipment is still in use or awaiting preparation, share current measurements and the planned transport state separately. We can review an FCL requirement without assuming that a catalogue dimension describes the unit that will be loaded.',
            ]),
            section('UK collection details to send before booking', bullets=[
                'Seller or warehouse address and the person responsible for collection handover.',
                'Ready-for-transport dimensions, gross weight and packaging details.',
                'Whether loading is included by the seller and what lifting equipment is available.',
                'Photographs of the equipment, its transport base and access to the loading area.',
                'Commercial shipment scope, readiness date and unloading needs in Lebanon.',
            ]),
            section('Example planning brief: a large machine purchased by a Lebanese business', [
                'A single machine may still be a suitable FCL inquiry. Send its dimensions and weight, the proposed packaging, and the pickup conditions so we can assess container fit and handling. Full Container Load describes dedicated container use; it does not require the goods to fill every available space.',
                'For smaller commercial goods, selected-route LCL from the UK into Lebanon may be reviewed. Compare the complete collection, handling, and delivery cost with an FCL plan. We confirm routing for the actual shipment rather than promising a direct sailing or a fixed transit time.',
            ]),
        ],
        'faqs': [
            ('Can one large machine from the UK be shipped as FCL?', 'Yes, subject to container fit, loading feasibility, and cargo acceptance. A dedicated container does not have to be completely full. Send dimensions, weight, packaging, and pickup conditions for review.'),
            ('What should we confirm with a UK machinery seller?', 'Confirm the collection location, release contact, transport-ready condition, and who is responsible for dismantling, packing, lifting, and loading. Include these responsibilities in the quote request.'),
            ('Do you provide LCL imports from the United Kingdom?', 'Yes. The United Kingdom is one of our selected LCL origins into Lebanon. Cargo acceptance, route, collection scope, and destination handling are confirmed for each shipment.'),
            ('Do you publish a fixed UK-to-Lebanon transit time?', 'No fixed transit time is promised on this page. Timing depends on the pickup, cargo readiness, confirmed route, carrier arrangements, and the agreed delivery scope.'),
        ],
    },
    {
        'slug': 'ukraine-to-lebanon-shipping.html', 'country': 'Ukraine',
        'title': 'Ukraine to Lebanon Freight | B2B FCL & Large Loads | AL MARWA CO',
        'description': 'B2B freight planning from Ukraine to Lebanon for full containers and large commercial cargo. Selected-route LCL imports with shipment-specific route review.',
        'heading': 'Ukraine to Lebanon Freight for Business Cargo',
        'intro': 'Plan a commercial shipment from Ukraine to Lebanon with the collection point and available routing reviewed before cargo is released. AL MARWA CO focuses on FCL, large business loads, and full truckloads by road. Ukraine is also within our selected origins for LCL imports into Lebanon.',
        'summary': 'Confirmed pickup points, route review and readiness windows.',
        'sections': [
            section('Confirm the practical starting point of the shipment', [
                'For Ukraine-origin cargo, provide the exact location where the goods can be handed over, the release contact, and the earliest realistic loading date. If a supplier proposes another handoff location, identify which transport steps the supplier covers and which steps you want us to assess.',
                'We confirm the collection point, route and handling plan for each shipment before cargo is released, so your receiving date is based on an actual plan rather than an estimate.',
            ]),
            section('Prepare a route review with clear handoff details', bullets=[
                'Actual pickup or proposed handoff address and responsible business contact.',
                'Cargo description, package list, gross weights and packed dimensions.',
                'Required FCL, FTL or LCL assessment and any special loading requirements.',
                'Cargo readiness window and the supplier arrangements already agreed.',
                'Lebanese delivery location and the receiving team’s timing constraints.',
            ]),
            section('Example planning brief: a commercial order awaiting release', [
                'For an order that is ready at a supplier site, send the packing list together with the proposed handoff arrangement. Explain whether the supplier is holding the cargo, arranging an initial transport leg, or waiting for your collection instructions. This avoids quoting the wrong starting point.',
                'We can then review the full-container requirement or assess selected-route LCL into Lebanon. For larger goods, include loading photographs and equipment needs. Route, schedule and price are confirmed for your shipment.',
            ]),
        ],
        'faqs': [
            ('Can you review a Ukraine-to-Lebanon FCL shipment?', 'Yes. Send the exact pickup or handoff location, cargo details, packing list, loading requirements, and readiness window. We review the proposed route and scope before confirming the shipment.'),
            ('Do you run full truckloads from Ukraine to Lebanon?', 'Yes. Ukraine is one of our full-truckload lanes alongside FCL. Send the pickup address, cargo details and readiness window, and we confirm the routing, vehicle and timing for your shipment.'),
            ('Is Ukraine included in your selected LCL origins?', 'Yes. We accept inquiries for LCL imports from Ukraine into Lebanon, subject to cargo acceptance, shipment-specific routing, and service confirmation.'),
            ('What if the supplier offers a different handoff location?', 'Share that address and explain which transport steps the supplier is arranging. We will review the requested scope from the actual handoff point rather than assume collection starts at the supplier’s business address.'),
        ],
    },
]


SERVICE_PAGES = [
    {
        'slug': 'full-truckload-lebanon.html',
        'title': 'Full Truckload Lebanon | B2B FTL Freight | AL MARWA CO',
        'description': 'Full truckload freight for businesses shipping substantial commercial cargo to or from Lebanon. FTL route reviews, machinery, loading and delivery planning.',
        'heading': 'Full Truckload Freight for Businesses in Lebanon',
        'intro': 'Full truckload (FTL) is a core part of our B2B offer: we run full trucks into Lebanon from Ukraine, Jordan, Iraq, the UAE, Turkey, the United Kingdom and China. AL MARWA CO reviews your pickup and delivery sites, cargo dimensions, weight, and loading requirements to define a workable truckload scope. FCL remains our specialty for worldwide container shipping.',
        'eyebrow': 'B2B · FTL · Full commercial loads', 'shipment': 'FTL',
        'summary': 'Full vehicles, loading access and commercial delivery scope.',
        'sections': [
            section('A truckload plan begins with the load and the sites', [
                'FTL means planning a vehicle around a shipper’s load. It can suit wholesale stock, palletized goods, machinery, or large orders when the cargo and road route support it. There is no fixed weight or volume threshold published here: space, weight distribution, loading access, and the goods themselves determine the equipment requirement.',
                'Tell us whether the shipment needs side, rear, or overhead loading, whether the goods can be stacked, and what equipment is available at both sites. A total weight alone is not enough to select a vehicle or define the loading responsibility.',
            ]),
            section('Our full-truckload lanes', [
                'We run full truckloads between Lebanon and Ukraine, Jordan, Iraq, the UAE, Turkey, the United Kingdom, and China, mostly for imports into Lebanon. On the longer lanes, such as China and the UK, we can also price FCL sea freight so you can compare cost and timing side by side.',
                'An offer should identify collection, transport, handling, documentation coordination, and final delivery where those tasks are requested. Confirm who loads and unloads, which site appointments are included, and how changes to cargo readiness will be handled.',
            ]),
            section('Send a complete FTL brief', bullets=[
                'Company name, origin and destination addresses, and site contacts.',
                'Itemized cargo dimensions, gross weights, pallet count and stacking restrictions.',
                'Vehicle count or equipment preference, if already specified.',
                'Loading method, access limits and unloading equipment.',
                'Readiness date, delivery window, shipment frequency and requested service scope.',
            ]),
        ],
        'faqs': [
            ('What does FTL mean?', 'FTL means Full Truckload: a vehicle is planned around one shipper’s load. The appropriate vehicle and route depend on the cargo profile, loading requirements, and available road service.'),
            ('Which countries do you run full truckloads from?', 'Our full-truckload lanes connect Lebanon with Ukraine, Jordan, Iraq, the UAE, Turkey, the United Kingdom and China, mostly for imports into Lebanon. For other countries, FCL is usually the better option, and FCL is our worldwide specialty.'),
            ('Can a truckload include machinery or non-stackable goods?', 'We can assess these loads using the dimensions and weight of each piece, loading photographs, stacking restrictions, and the equipment available at the pickup and delivery sites.'),
            ('What changes the scope of an FTL quote?', 'Collection and delivery locations, vehicle needs, site access, loading and unloading tasks, shipment readiness, documentation coordination, and the confirmed road route all affect the scope.'),
        ],
    },
    {
        'slug': 'heavy-equipment-shipping-lebanon.html',
        'title': 'Heavy Equipment Shipping Lebanon | B2B Large Cargo | AL MARWA CO',
        'description': 'B2B shipping for machinery, industrial equipment and large cargo in Lebanon. FCL fit reviews, full-load transport and lifting, loading and delivery planning.',
        'heading': 'Machinery & Large Cargo Shipping for Businesses',
        'intro': 'Shipping production equipment, a large tank, or an industrial machine starts with a practical loading plan. AL MARWA CO focuses on large commercial cargo, FCL worldwide, and full truckloads on our seven core lanes. We review the transport dimensions, weight, lifting needs, and site access before confirming a freight option.',
        'eyebrow': 'B2B · Machinery · Large commercial cargo', 'shipment': 'Large Cargo',
        'summary': 'Container fit, transport preparation, lifting and site access.',
        'sections': [
            section('Review the transport unit, not just the product', [
                'A machine’s working dimensions may differ from its transport dimensions. Tell us whether it will be dismantled, crated, secured to a base, or moved as one unit. List any loose attachments separately. The lifting points, transport orientation, and weight of each piece help establish how it can be loaded.',
                'For a tank or equipment previously used with liquids or other materials, describe its previous contents and current condition. Acceptance and any additional handling requirements must be reviewed before booking. Photographs and drawings help us understand the cargo; they do not replace the final packing and weight information.',
            ]),
            section('FCL can be practical for one large commercial item', [
                'A dedicated container does not have to be completely full. One large item can be reviewed as an FCL shipment when its size, weight, loading method, and route make that practical. This is how we assess large business cargo from origins outside our main import markets as well.',
                'If the item does not fit standard container handling, we assess whether a suitable equipment and handling plan is available. The quote sets out the container or vehicle, lifting, loading and delivery scope we have agreed with you.',
            ]),
            section('What to send for a machinery freight review', bullets=[
                'Length, width, height and gross weight of every transportable piece.',
                'Current photographs, packaging plan, drawings and identified lifting points.',
                'Whether the equipment can be tilted, stacked or dismantled.',
                'Pickup and delivery access, including clearances and ground-level handling needs.',
                'Who provides dismantling, packing, crane work, loading and unloading.',
                'Cargo readiness, project deadline and the company receiving the equipment.',
            ]),
        ],
        'faqs': [
            ('Can you ship one large tank or machine from another country?', 'We can review it as a business FCL shipment, subject to container fit, loading feasibility, cargo acceptance, and route availability. Send its dimensions, weight, condition, photographs, and pickup details.'),
            ('Do you guarantee that oversized equipment fits a container?', 'No. Fit and loading feasibility are assessed using the actual transport dimensions, weight, lifting arrangements, and available equipment. A proposed option is confirmed only after that review.'),
            ('What details matter for a used tank?', 'Describe its previous contents, present condition, transport dimensions, weight, packaging, and lifting points. Any acceptance and handling requirements are confirmed before booking.'),
            ('Can the quote include lifting and site handling?', 'Tell us which lifting, loading, unloading, or placement tasks you need. We review site access and equipment requirements, then define which tasks can be included in the agreed scope.'),
        ],
    },
    {
        'slug': 'lcl-shipping-lebanon.html',
        'title': 'LCL Imports to Lebanon | Seven B2B Origin Markets | AL MARWA CO',
        'description': 'LCL shipping into Lebanon from China, Turkey, UAE, Jordan, Iraq, Ukraine and the UK. Commercial cargo review, packing details and full-cost comparison with FCL.',
        'heading': 'LCL Imports to Lebanon from Selected Business Markets',
        'intro': 'LCL (Less than Container Load) shares container space with other shipments. AL MARWA CO offers LCL imports into Lebanon from seven selected origins: Ukraine, Jordan, Iraq, the UAE, Turkey, the United Kingdom, and China. Our main specialty remains FCL worldwide for substantial commercial loads.',
        'eyebrow': 'B2B · Selected-origin LCL imports', 'shipment': 'LCL',
        'summary': 'Smaller commercial loads from seven selected origins into Lebanon.',
        'sections': [
            section('Confirm the origin and direction before comparing prices', [
                'Our LCL coverage is for the seven named origin markets into Lebanon. It is not a worldwide shared-container offer, and it does not imply LCL exports from Lebanon to every destination. Cargo acceptance, collection arrangements, consolidation, routing, and availability are confirmed for the actual shipment.',
                'For a large item from another origin, ask us to review an FCL solution. We assess dedicated-container use around the cargo and loading requirements, even when a single item does not occupy the whole container.',
            ]),
            section('Compare the complete LCL and FCL scope', [
                'A smaller shipment does not automatically produce a lower total cost. Ask which collection, consolidation, handling, destination, and delivery steps are included. A useful comparison uses the same origin and final destination for both options and identifies any services still to be arranged.',
                'FCL provides dedicated container use. LCL includes shared-container handling, so packaging, dimensions, stacking limits, and readiness information need to be clear. For machinery, non-stackable pieces, or recurring orders approaching a container load, ask us to review the FCL alternative.',
            ]),
            section('Prepare a commercial LCL inquiry', bullets=[
                'Your company, one of the seven origin countries, and the Lebanese delivery address.',
                'Goods description, package count, packed dimensions and gross weight.',
                'Pallet or crate details and any restrictions on stacking or orientation.',
                'Cargo readiness and the collection or warehouse handoff requested.',
                'Customs documentation and final-delivery coordination needed in the scope.',
            ]),
        ],
        'faqs': [
            ('Which origins do you offer LCL imports from?', LCL_SCOPE),
            ('Do you offer LCL from Australia or Germany into Lebanon?', 'Those countries are outside our published LCL origin coverage. For a large business item or a substantial load, ask us to assess an FCL shipment instead.'),
            ('Can we export LCL from Lebanon worldwide?', 'Our published LCL offer is limited to the seven selected origins into Lebanon. Our worldwide specialty is FCL, including full-container exports from Lebanon.'),
            ('Is LCL always the lower-cost option?', 'No. Compare collection, consolidation, handling, destination, and delivery charges for the same service scope. Shipment size, packaging, handling requirements, and route availability determine the practical comparison.'),
        ],
    },
    {
        'slug': 'export-shipping-lebanon.html',
        'title': 'Export from Lebanon | Worldwide B2B FCL Shipping | AL MARWA CO',
        'description': 'Worldwide FCL exports from Lebanon for manufacturers, exporters and businesses moving full containers or large cargo. Loading, document and delivery planning.',
        'heading': 'Worldwide FCL Exports from Lebanon for Businesses',
        'intro': 'AL MARWA CO helps Lebanese manufacturers, exporters, traders, and project teams plan full-container shipments worldwide. Our specialty is FCL for substantial commercial cargo, machinery, and business stock. Share the actual destination and requested delivery scope so we can review the route and loading plan.',
        'eyebrow': 'Lebanon to the world · B2B FCL', 'shipment': 'FCL',
        'origin': 'Lebanon', 'destination': '',
        'summary': 'Full-container exports, receiving scope and buyer handover.',
        'sections': [
            section('Define where your export responsibility ends', [
                'An export quote is easier to compare when the shipper and buyer agree on the requested handoff. Tell us whether you need pickup in Lebanon, container loading coordination, port-to-port movement, or a broader destination delivery scope. Share any agreed Incoterms so the proposal can reflect the commercial arrangement.',
                'The destination country alone is not enough to define final delivery. Provide the receiving business address, contact, unloading conditions, and any known appointment or site constraints. Destination service and cargo acceptance are checked for the particular shipment.',
            ]),
            section('Prepare a load plan before the goods leave Lebanon', [
                'Send an itemized packing list with packed dimensions, gross weights, and stacking limits. For multiple product lines or machines, identify anything that must stay upright or needs separate lifting. The container type and count should reflect the actual transport units, not an estimate based only on the order value.',
                'Tell us when the full order will be ready and who will load it. Where a shipment includes machinery or large equipment, provide photographs, loading points, and site access details. We review the requested container and inland handling scope before booking.',
            ]),
            section('Information for a Lebanon export quote', bullets=[
                'Exporter and receiving company, with pickup and destination addresses.',
                'Goods description, packed dimensions, package count and gross weight.',
                'Container type and count, or the full cargo data if undecided.',
                'Readiness date, buyer deadline and expected shipment frequency.',
                'Agreed Incoterms and requested pickup, documentation, freight and delivery scope.',
            ]),
        ],
        'faqs': [
            ('Do you arrange FCL exports from Lebanon worldwide?', 'Worldwide FCL exports from Lebanon are part of our main B2B specialty. Each destination, cargo acceptance, route, schedule, and requested service scope is confirmed for the shipment.'),
            ('Can we request final delivery at the buyer’s premises?', 'Yes, as a requested scope for review. Send the receiving address, site contact, unloading needs, and any delivery constraints. We confirm which destination services can be included.'),
            ('What if we do not know the container count yet?', 'Send an itemized packing list with packed dimensions, weights, and stacking restrictions. We can review the container requirement and any loading issues using that information.'),
            ('Does worldwide export coverage include LCL to every country?', 'Our worldwide specialty is FCL. The published LCL offer covers imports into Lebanon from seven selected origins, rather than worldwide LCL exports.'),
        ],
    },
]


def paragraphs(items):
    return '\n'.join(f'<p>{escape(p)}</p>' for p in items)


def bullets(items):
    return '<ul>' + ''.join(f'<li>{escape(p)}</li>' for p in items) + '</ul>' if items else ''


def link(href, label, primary=False):
    return f'<a href="{escape(href, quote=True)}" class="button{" primary" if primary else ""}">{escape(label)}</a>'


def route_cards():
    return '<div class="freight-route-grid">' + ''.join(
        f'<a class="freight-route-link" href="{r["slug"]}"><h3>{escape(r["country"])} to Lebanon <span aria-hidden="true">↗</span></h3><p>{escape(r["summary"])}</p></a>' for r in ROUTES
    ) + '</div>'


HUB = {
    'slug': 'shipping-routes-lebanon.html',
    'title': 'Lebanon Shipping Routes | B2B Imports & FCL Exports | AL MARWA CO',
    'description': 'Explore B2B import routes into Lebanon from seven key markets, selected-origin LCL, full truckloads and worldwide FCL exports for large commercial cargo.',
    'heading': 'Business Freight Routes into Lebanon & FCL Exports Worldwide',
    'intro': 'Find the right starting point for your commercial shipment. Our key import markets are Ukraine, Jordan, Iraq, the UAE, Turkey, the United Kingdom, and China. FCL worldwide is our specialty, with full truckloads on our seven core lanes and LCL offered from these selected origins into Lebanon.',
    'eyebrow': 'B2B import routes · Worldwide FCL exports', 'shipment': 'FCL',
    'summary': 'The seven key import markets and the correct service scope.',
    'sections': [
        section('Match the freight service to the direction of travel', [
            'For full containers, we review commercial imports to Lebanon from worldwide origins and exports from Lebanon worldwide. The seven markets below are our main import focus. A country outside that list can still be considered for an FCL shipment, including a single large business item where container fit and total handling cost make sense.',
            LCL_SCOPE + ' Each country page explains what to send for a fast, accurate quote. Routing, schedule and price are confirmed for your shipment.',
        ]),
        section('Choose a route brief that answers your pickup questions', [
            'The China page covers supplier and order readiness; Turkey covers packed loads and factory access; the UAE page explains warehouse handover details. Jordan and Iraq focus on site access and full-load collection information. The UK page covers machinery purchases, while the Ukraine page helps identify the actual handoff point for a route review.',
            'Each page lists the information needed to assess that shipment. Use the route that matches the actual origin of the goods, then include your company, load size, readiness date, and delivery requirements in the quote request.',
        ]),
    ],
    'faqs': [
        ('What are your main import routes into Lebanon?', f'Our main import markets are {ORIGINS}. We focus on B2B FCL and large commercial loads, with LCL from these origins into Lebanon and full truckloads on our seven core lanes.'),
        ('Can a business ship FCL from another country?', 'Yes. Worldwide FCL is our specialty. Send the origin, destination, cargo dimensions, weight, loading needs, and readiness date so we can review the route and total service scope.'),
        ('Do you run full truckloads on these routes?', 'Yes. We run full truckloads by road from all seven markets into Lebanon, alongside FCL. For each shipment we confirm routing, vehicle, schedule and price before booking.'),
        ('Do you also ship from Lebanon to other countries?', 'Yes. We coordinate FCL exports from Lebanon worldwide. Destination acceptance, route, schedule, and the requested pickup and delivery scope are confirmed for each shipment.'),
    ],
}


def render_page(spec, template):
    source_schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', template, re.S)[1])
    shared=deepcopy([n for n in source_schema['@graph'] if n['@type'] in ['LocalBusiness','WebSite']])
    url=BASE+spec['slug']
    is_route='country' in spec
    is_hub=spec['slug']==HUB['slug']
    language=spec.get('language','en')
    locale=spec.get('locale','en-LB')
    kind=spec.get('kind','service')
    content_id=url+{'service':'#service','guide':'#article','collection':'#resources','tool':'#tool'}[kind]
    is_ar=language=='ar'
    crumb_parent=spec.get('parent',('shipping-routes-lebanon.html','مسارات الشحن' if is_ar else 'Shipping Routes') if is_route else ('services.html','Freight Services'))
    if is_hub:
        crumb_parent=None
    breadcrumb_items=[{'@type':'ListItem','position':1,'name':'Home','item':BASE}]
    if crumb_parent:
        breadcrumb_items.append({'@type':'ListItem','position':2,'name':crumb_parent[1],'item':BASE+crumb_parent[0]})
    short_names = {
        'shipping-routes-lebanon.html': 'Shipping Routes',
        'full-truckload-lebanon.html': 'Full Truckloads',
        'heavy-equipment-shipping-lebanon.html': 'Machinery & Large Cargo',
        'lcl-shipping-lebanon.html': 'Selected-Origin LCL',
        'export-shipping-lebanon.html': 'FCL Exports from Lebanon',
    }
    crumb_label = (f'من {spec["country"]} إلى لبنان' if is_ar else spec['country']+' to Lebanon') if is_route else short_names.get(spec['slug'],spec.get('short_name',spec['heading']))
    breadcrumb_items.append({'@type':'ListItem','position':len(breadcrumb_items)+1,'name':crumb_label,'item':url})
    graph=shared+[
        {'@type':'WebPage','@id':url+'#webpage','url':url,'name':spec['title'],'description':spec['description'],
         'inLanguage':locale,'isPartOf':{'@id':BASE+'#website'},'about':{'@id':BASE+'#organization'},
         'publisher':{'@id':BASE+'#organization'},'mainEntity':{'@id':content_id},
         'hasPart':{'@id':url+'#faq'},'breadcrumb':{'@id':url+'#breadcrumb'}},
        {'@type':'Service','@id':url+'#service','url':url,'name':spec['heading'],'description':spec['intro'],
         'serviceType':['B2B FCL imports','Selected-origin LCL imports'] if is_route else spec['heading'],
         'provider':{'@id':BASE+'#organization'},'mainEntityOfPage':{'@id':url+'#webpage'},
         'audience':{'@type':'BusinessAudience','audienceType':spec.get('audience','Importers, exporters, wholesalers, manufacturers and project teams')},
         'areaServed':[{'@type':'Country','name':spec.get('quote_origin',spec['country'])},{'@type':'Country','name':'Lebanon'}] if is_route else {'@type':'Place','name':'Lebanon and international freight routes'}},
        {'@type':'FAQPage','@id':url+'#faq','isPartOf':{'@id':url+'#webpage'},'inLanguage':locale,
         'mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in spec['faqs']]},
        {'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':breadcrumb_items},
    ]
    if kind!='service':
        graph=[n for n in graph if n.get('@type')!='Service']
        content={'@id':content_id,'name':spec['heading'],'description':spec['intro'],'url':url}
        if kind=='guide':
            content.update({'@type':'Article','headline':spec['heading'],'inLanguage':locale,'author':{'@id':BASE+'#organization'},'publisher':{'@id':BASE+'#organization'},'mainEntityOfPage':{'@id':url+'#webpage'}})
        elif kind=='tool':
            content.update({'@type':'WebApplication','applicationCategory':'BusinessApplication','operatingSystem':'Any','inLanguage':locale,'publisher':{'@id':BASE+'#organization'}})
        else:
            content.update({'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i,'name':name,'url':BASE+path} for i,(path,name) in enumerate([
                ('freight-planner-lebanon.html','Business freight planner'),('cargo-volume-calculator.html','Cargo volume calculator'),('container-shipping-costs-lebanon.html','Container quote cost guide'),('beirut-freight-guide.html','Beirut freight planning guide')],1)]})
        graph.append(content)
    if is_hub:
        graph.append({'@type':'ItemList','@id':url+'#routes','name':'Key B2B import routes into Lebanon','itemListElement':[
            {'@type':'ListItem','position':i,'name':r['country']+' to Lebanon','url':BASE+r['slug']} for i,r in enumerate(ROUTES,1)]})
    schema=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,indent=2)
    header=header_markup(language,spec['slug'])
    footer=re.search(r'        <footer id="footer">.*?</footer>',template,re.S)[0]
    whatsapp=re.search(r'    <a href="https://wa.me/.*?</a>',template,re.S)[0]
    body_sections='\n'.join(
        f'<section class="freight-panel"><h2>{escape(s["title"])}</h2>{paragraphs(s["paragraphs"])}{bullets(s["bullets"])}{s.get("html", "")}</section>' for s in spec['sections']
    )
    origin=spec.get('quote_origin',spec.get('country',spec.get('origin','')))
    destination=spec.get('destination','Lebanon')
    shipment=spec.get('shipment','FCL')
    main_quote=quote_url(shipment,origin,destination)
    parent_href,parent_name=crumb_parent or ('index.html','Home')
    crumb=f'<nav class="freight-breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a> / '+(f'<a href="{parent_href}">{parent_name}</a> / ' if crumb_parent else '')+f'<span aria-current="page">{escape(crumb_label)}</span></nav>'
    mode_section=''
    if is_route:
        mode_section=f'''<section class="freight-panel" aria-labelledby="mode-title">
<h2 id="mode-title">Service scope for {escape(origin)} to Lebanon</h2>
<dl class="freight-service-facts">
<div><dt>FCL · Full Container Load</dt><dd>Our specialty for substantial business loads, machinery and dedicated container use.</dd></div>
<div><dt>LCL · Less than Container Load</dt><dd>{escape(origin)} is a selected LCL import origin into Lebanon. Shipment acceptance and arrangements are confirmed per inquiry.</dd></div>
<div><dt>FTL · Full Truckload</dt><dd>Full truckloads by road from {escape(origin)} into Lebanon are part of our core service. Vehicle and loading are planned around your cargo.</dd></div>
</dl><p>Based on Khalde Highway since 1997, we coordinate the shipment scope with your business, supplier, and receiving team.</p>
</section>'''
    if is_route and is_ar:
        c=escape(spec['country'])
        mode_section=f'''<section class="freight-panel" aria-labelledby="mode-title">
<h2 id="mode-title">خدماتنا من {c} إلى لبنان</h2>
<dl class="freight-service-facts">
<div><dt>FCL · حاوية كاملة</dt><dd>تخصصنا الأساسي للحمولات التجارية الكبيرة والماكينات والحاويات المخصصة لشحنة واحدة.</dd></div>
<div><dt>FTL · شاحنة كاملة</dt><dd>شاحنات كاملة برّاً من {c} إلى لبنان ضمن خدماتنا الأساسية، مع تخطيط الشاحنة والتحميل حول بضاعتك.</dd></div>
<div><dt>LCL · شحن جزئي</dt><dd>{c} من الدول السبع التي نوفر منها الشحن الجزئي إلى لبنان، مع تأكيد قبول البضاعة لكل طلب.</dd></div>
</dl><p>من مكتبنا على أوتوستراد خلدة منذ 1997، ننسّق الشحنة مع شركتك والمورّد وفريق الاستلام.</p>
</section>'''
    if is_hub:
        mode_section='<section class="freight-panel"><h2>Explore the seven key import markets</h2>'+route_cards()+'</section>'
    if spec['slug']=='lcl-shipping-lebanon.html':
        mode_section='<section class="freight-panel"><h2>Selected LCL origins into Lebanon</h2>'+route_cards()+'</section>'
    related=[('sea-freight-lebanon.html','FCL worldwide'),('full-truckload-lebanon.html','Full truckloads'),('heavy-equipment-shipping-lebanon.html','Machinery & large cargo'),('lcl-shipping-lebanon.html','Selected-origin LCL'),('export-shipping-lebanon.html','Exports from Lebanon'),('shipping-routes-lebanon.html','All import routes')]
    related=[(href,label) for href,label in related if href!=spec['slug']]
    related_markup=''.join(f'<a href="{href}">{escape(label)} <span aria-hidden="true">↗</span></a>' for href,label in related)
    faq=''.join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q,a in spec['faqs'])
    secondary=link(quote_url('LCL',origin,'Lebanon'),'Ask about LCL imports') if is_route else link('shipping-routes-lebanon.html','Explore import routes')
    if is_hub:
        secondary=link('export-shipping-lebanon.html','Plan an FCL export')
    alternates=spec.get('alternates',{})
    alternate_links=''.join(f'    <link rel="alternate" hreflang="{loc}" href="{href}" />\n' for loc,href in alternates.items())
    switch=''
    if spec.get('switch'):
        href,label,lang_code=spec['switch']
        direction=' dir="rtl"' if lang_code=='ar' else ' dir="ltr"'
        switch=f'<p class="freight-language-switch"><a href="{href}" lang="{lang_code}" hreflang="{lang_code}-LB"{direction}>{escape(label)}</a></p>'
    ar_routes=''
    if is_route and is_ar:
        from routes_ar import ROUTES_AR
        ar_routes='<nav class="freight-panel freight-related freight-related-ar" aria-label="مسارات أخرى"><h2>مسارات أخرى إلى لبنان</h2>'+''.join(
            f'<a href="{r["slug"]}">من {escape(r["country"])} إلى لبنان <span aria-hidden="true">↖</span></a>' for r in ROUTES_AR if r['slug']!=spec['slug'])+'<a href="fcl-shipping-lebanon-ar.html">شحن الحاويات الكاملة FCL</a><a href="freight-forwarding-beirut-ar.html">شحن الشركات في بيروت</a></nav>'
    tools_scripts='''<script src="assets/js/freight-tools-core.js" defer></script><script src="assets/js/freight-tools.js" defer></script>''' if kind=='tool' else ''
    html=f'''<!DOCTYPE HTML>
<html lang="{language}"{' dir="rtl"' if language=='ar' else ''}>
<head>
    <meta charset="utf-8" />
    <title>{escape(spec['title'])}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <meta name="description" content="{escape(spec['description'],quote=True)}" />
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
    <meta name="author" content="AL MARWA CO" />
    <meta name="theme-color" content="#0b4d2b" />
    <link rel="canonical" href="{url}" />
{alternate_links}    <link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32x32.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="images/apple-touch-icon.png" />
    <meta property="og:locale" content="{locale.replace('-', '_')}" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="AL MARWA CO" />
    <meta property="og:title" content="{escape(spec['title'],quote=True)}" />
    <meta property="og:description" content="{escape(spec['description'],quote=True)}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{BASE}images/hero-beirut.jpg" />
    <meta property="og:image:alt" content="Container vessel approaching the Port of Beirut" />
    <meta property="og:image:width" content="1672" />
    <meta property="og:image:height" content="941" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{escape(spec['title'],quote=True)}" />
    <meta name="twitter:description" content="{escape(spec['description'],quote=True)}" />
    <meta name="twitter:image" content="{BASE}images/hero-beirut.jpg" />
    <meta name="twitter:image:alt" content="Container vessel approaching the Port of Beirut" />
    <script type="application/ld+json">
{schema}
    </script>
    <link rel="stylesheet" href="assets/css/fonts.css" />
    <link rel="stylesheet" href="assets/css/fontawesome-all.min.css" />
    <link rel="stylesheet" href="assets/css/main.css" />
    <link rel="stylesheet" href="assets/css/freight-pages.css" />
    <link rel="preload" href="images/hero-beirut.webp" as="image" type="image/webp" fetchpriority="high" />
    <noscript><link rel="stylesheet" href="assets/css/noscript.css" /></noscript>
</head>
<body class="is-preload freight-page">
    <a href="#main" class="skip-link">Skip to main content</a>
    <div id="wrapper">
{header}
        <section class="freight-hero" aria-labelledby="freight-title">
            <div class="inner">
                {crumb}
                <p class="freight-eyebrow">{escape(spec.get('eyebrow','B2B imports · FCL first · Large commercial loads'))}</p>
                <h1 id="freight-title">{escape(spec['heading'])}</h1>
                <p class="freight-intro">{escape(spec['intro'])}</p>{switch}
                <div class="freight-actions">{link(main_quote,'Request a B2B freight quote',True)}{secondary}</div>
            </div>
        </section>
        <main id="main" class="freight-main">
            <div class="inner freight-layout">
                <div class="freight-content">
                    {mode_section}
                    {body_sections}
                    <section class="freight-panel freight-faq" aria-labelledby="freight-faq-title"><h2 id="freight-faq-title">Business freight questions</h2>{faq}</section>
                    <section class="freight-closing"><p class="freight-eyebrow">Plan the commercial load</p><h2>Send a shipment brief your team can work from</h2><p>Share your company, route, container or truck count, packed dimensions, gross weight, readiness date, and requested pickup and delivery scope. For large equipment, include photographs and loading details.</p><div class="freight-actions">{link(main_quote,'Request a B2B freight quote',True)}{link('tel:+96170099978','Call +961 70 099978')}</div></section>
                </div>
                <aside class="freight-aside" aria-label="Related services and freight desk">
                    <section class="freight-panel"><p class="freight-eyebrow">Your business freight desk</p><h2>AL MARWA CO</h2><p>B2B freight since 1997.<br>Khalde Highway, Lebanon.<br>Serving Beirut and businesses across Lebanon.</p><a href="tel:+96170099978">+961 70 099978</a><br><a href="mailto:info@al-marwaco.com">info@al-marwaco.com</a></section>
                    {ar_routes}<nav class="freight-panel freight-related" aria-label="Related freight pages"><h2>Explore the right service</h2>{related_markup}<a href="beirut-freight-guide.html">Shipment planning guide <span aria-hidden="true">↗</span></a></nav>
                </aside>
            </div>
        </main>
{footer}
    </div>
{whatsapp}
    <script src="assets/js/browser.min.js" defer></script>
    <script src="assets/js/breakpoints.min.js" defer></script>
    <script src="assets/js/main.js" defer></script>
    <script src="assets/js/freight-pages.js" defer></script>
    {tools_scripts}
</body>
</html>
'''
    if language=='ar':
        translations={
            'Skip to main content':'الانتقال إلى المحتوى',
            'Request a B2B freight quote':'اطلب عرض شحن للشركات',
            'Ask about LCL imports':'اسأل عن الشحن الجزئي LCL',
            'Explore import routes':'مسارات الاستيراد (English)',
            'Business freight questions':'أسئلة عن شحن الشركات',
            'Plan the commercial load':'تخطيط الحمولة التجارية',
            'Send a shipment brief your team can work from':'أرسل تفاصيل الحمولة لبدء المراجعة',
            'Share your company, route, container or truck count, packed dimensions, gross weight, readiness date, and requested pickup and delivery scope. For large equipment, include photographs and loading details.':'أرسل اسم الشركة والمسار وعدد الحاويات أو الشاحنات والأبعاد بعد التغليف والوزن الإجمالي وتاريخ الجاهزية ونطاق الاستلام والتسليم المطلوب. للمعدات الكبيرة، أرفق وصفاً واضحاً للتحميل والصور أو الرسومات المتاحة.',
            'Call +961 70 099978':'اتصل على +961 70 099978',
            'Your business freight desk':'فريق شحن الشركات',
            'B2B freight since 1997.':'شحن للشركات منذ 1997.',
            'Khalde Highway, Lebanon.':'أوتوستراد خلدة، لبنان.',
            'Serving Beirut and businesses across Lebanon.':'نخدم الشركات في بيروت ومختلف المناطق اللبنانية.',
            'Explore the right service':'أدلة الخدمات باللغة الإنجليزية',
            'Shipment planning guide':'دليل تخطيط الشحن (English)',
        }
        for old,new in translations.items():html=html.replace(old,new)
        html=html.replace('<a href="index.html">Home</a> /','<a href="index.html">الرئيسية</a> /')
        # Shared English footer and service titles declare their actual language.
        html=html.replace('<footer id="footer">','<footer id="footer" lang="en" dir="ltr">')
        html=html.replace('class="freight-panel freight-related"','class="freight-panel freight-related" lang="en" dir="ltr"')
    return html


def main():
    from business_content import BUSINESS_PAGES
    template=(ROOT/'sea-freight-lebanon.html').read_text(encoding='utf-8')
    from routes_ar import ROUTES_AR
    for ar in ROUTES_AR:
        en=next(r for r in ROUTES if r['slug']==ar['en_slug'])
        pair={'en-LB':BASE+en['slug'],'ar-LB':BASE+ar['slug'],'x-default':BASE+en['slug']}
        en['alternates']=ar['alternates']=pair
        en['switch']=(ar['slug'],'اقرأ هذه الصفحة بالعربية','ar')
        ar['switch']=(en['slug'],'Read this page in English','en')
    for spec in [HUB]+ROUTES+ROUTES_AR+SERVICE_PAGES+BUSINESS_PAGES:
        (ROOT/spec['slug']).write_text(render_page(spec,template),encoding='utf-8')
    print(f'Built {1+len(ROUTES)+len(ROUTES_AR)+len(SERVICE_PAGES)+len(BUSINESS_PAGES)} service, route and planning pages.')


if __name__=='__main__':
    main()
