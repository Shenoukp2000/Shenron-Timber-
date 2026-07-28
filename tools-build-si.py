#!/usr/bin/env python3
"""Generate si/index.html — the Sinhala twin of the English homepage.

Works by substituting visible English strings in index.html, so the
markup, SVG and layout stay byte-identical to the English page and the
two can never drift apart structurally.
"""
import pathlib, re

ROOT = pathlib.Path("/Users/shenoukperera/Desktop/personal website/hands_website_claude_pack/shenron-timber")
src = (ROOT / "index.html").read_text()

# Longest-first ordering matters: replace whole sentences before fragments.
T = [
# ---- nav / chrome
('>Estates</a>', '>වතු</a>'),
('>Products</a>', '>නිෂ්පාදන</a>'),
('>Capacity</a>', '>ධාරිතාව</a>'),
('>Delivery</a>', '>බෙදාහැරීම</a>'),
('>Guides</a>', '>මාර්ගෝපදේශ</a>'),
('>Contact</a>', '>සම්බන්ධ වන්න</a>'),
('>Request a Quote</a>', '>මිල ගණන් ඉල්ලන්න</a>'),
('aria-label="Open menu"', 'aria-label="මෙනුව විවෘත කරන්න"'),

# ---- hero
('Plantation timber · Sabaragamuwa, Sri Lanka', 'වතු දැව · සබරගමුව, ශ්‍රී ලංකාව'),
('Plantation Timber, Firewood &amp; Biomass Supplier in Sri Lanka',
 'ශ්‍රී ලංකාවේ වතු දැව, දර සහ ජෛව ස්කන්ධ සැපයුම්කරු'),
('Standing timber at scale, from the wet-zone hills of Ratnapura',
 'රත්නපුර තෙත් කලාපීය කඳුකරයෙන්, විශාල පරිමාණයෙන් දැව'),
('Shenron Timber (Pvt) Ltd is a VAT-registered plantation timber company holding harvesting rights across six estates — supplying <strong>timber logs and firewood to buyers across Sri Lanka</strong>, from single loads to bulk contracts. Export enquiries welcome.',
 'ෂෙන්රොන් ටිම්බර් (පුද්) සමාගම යනු වතු හයක් හරහා දැව කැපීමේ අයිතිය හිමි, වැට් ලියාපදිංචි වතු දැව සමාගමකි. තනි ලොරි පැටවීමක සිට තොග ගිවිසුම් දක්වා, <strong>ශ්‍රී ලංකාව පුරා ගැනුම්කරුවන්ට ලී කොට සහ දර</strong> සපයමු. අපනයන විමසීම් ද පිළිගනිමු.'),
('>View Product Lines</a>', '>නිෂ්පාදන බලන්න</a>'),
('<span>Island-wide delivery</span>', '<span>දිවයින පුරා බෙදාහැරීම</span>'),
('<span>6 estates</span>', '<span>වතු 6ක්</span>'),
('<span>~67,000 MT standing volume</span>', '<span>මෙ.ටොන් 67,000ක් පමණ</span>'),
('<span>VAT-registered</span>', '<span>වැට් ලියාපදිංචි</span>'),
('<span>Export capable</span>', '<span>අපනයන හැකියාව</span>'),

# ---- about
('>About the company<', '>සමාගම ගැන<'),
('Six estates in the Sabaragamuwa hill country', 'සබරගමුව කඳුකරයේ වතු හයක්'),
('Shenron Timber operates across the wet-zone plantations of the Ratnapura district — high-rainfall hill country where Acacia mangium and Eucalyptus grow fast and dense. We purchase standing timber and hold the harvesting rights, managing felling, extraction, and haulage from estate to buyer.',
 'ෂෙන්රොන් ටිම්බර් කටයුතු කරන්නේ රත්නපුර දිස්ත්‍රික්කයේ තෙත් කලාපීය වතුයායවල් හරහාය — ඇකේෂියා මැංජියම් සහ යුකැලිප්ටස් ශීඝ්‍රයෙන් හා ඝනව වැඩෙන අධික වර්ෂාපතනයක් සහිත කඳුකරයයි. අපි සිටුවා ඇති දැව මිලදී ගෙන කැපීමේ අයිතිය දරමින්, කැපීම, ඉවත් කිරීම සහ වතුයායේ සිට ගැනුම්කරු දක්වා ප්‍රවාහනය කළමනාකරණය කරමු.'),
('Our resource base spans six estates under Hapugastenne Plantations PLC, a Browns Group company — giving buyers a single counterparty with plantation-scale volume and documented provenance.',
 'අපගේ සම්පත් පදනම බ්‍රවුන්ස් සමූහයේ සමාගමක් වන හපුගස්තැන්න ප්ලාන්ටේෂන්ස් PLC යටතේ ඇති වතු හයක් පුරා විහිදේ — එමඟින් ගැනුම්කරුවන්ට වතු පරිමාණයේ ධාරිතාවක් සහ ලේඛනගත මූලාශ්‍රයක් සහිත තනි පාර්ශ්වයක් ලැබේ.'),
('>Documented provenance<', '>ලේඛනගත මූලාශ්‍රය<'),
('Timber rights purchased from Browns Group / Hapugastenne Plantations PLC — plantation-grown, not natural forest.',
 'දැව අයිතිය බ්‍රවුන්ස් සමූහය / හපුගස්තැන්න ප්ලාන්ටේෂන්ස් PLC වෙතින් මිලදී ගෙන ඇත — වතුවල වගා කළ දැව මිස ස්වාභාවික වනාන්තර දැව නොවේ.'),
('<li>VAT-registered Sri Lankan company</li>', '<li>වැට් ලියාපදිංචි ශ්‍රී ලාංකික සමාගමකි</li>'),
('<li>Harvesting rights to standing timber across six estates</li>', '<li>වතු හයක සිටුවා ඇති දැව කැපීමේ අයිතිය</li>'),
('<li>Plantation species: Acacia, Eucalyptus, Mahogany</li>', '<li>වතු විශේෂ: ඇකේෂියා, යුකැලිප්ටස්, මහෝගනී</li>'),
('<li>Volumes verified by estate enumeration</li>', '<li>වතුයාය ගණන් කිරීම් මගින් තහවුරු කළ ධාරිතාව</li>'),

# ---- products
('>Product lines<', '>නිෂ්පාදන පෙළ<'),
('Two product lines, one source', 'නිෂ්පාදන පෙළ දෙකක්, එක් මූලාශ්‍රයක්'),
('Firewood by the tonne for tea factories, bakeries, kilns and brick works; timber logs and sawlogs for sawmills, timber merchants and furniture makers. Ask for either — or both — in one quote request.',
 'තේ කර්මාන්තශාලා, බේකරි, උදුන් සහ ගඩොල් කර්මාන්ත සඳහා ටොන් ගණනින් දර; වඩු කර්මාන්තශාලා, ලී වෙළෙන්දන් සහ ගෘහ භාණ්ඩ නිෂ්පාදකයන් සඳහා ලී කොට සහ ඉරන ලී. එකක් හෝ දෙකම එකම මිල ඉල්ලීමකින් ඉල්ලන්න.'),
('Line 01 · Sold by weight (MT / kg)', 'පෙළ 01 · බර අනුව විකිණේ (මෙ.ටොන් / කි.ග්‍රෑ)'),
('Firewood &amp; Biomass Logs', 'දර සහ ජෛව ස්කන්ධ ලී කොට'),
('High-calorific fast-grown hardwood — the workhorse of boiler fuel and industrial firewood.',
 'ඉහළ තාප අගයක් සහිත ශීඝ්‍රයෙන් වැඩෙන දැඩි දැව — බොයිලේරු ඉන්ධන සහ කාර්මික දර සඳහා ප්‍රධානතම තේරීම.'),
('Dense-burning eucalypt, well suited to fuelwood and biomass chip supply.',
 'ඝනව දැවෙන යුකැලිප්ටස් වර්ගයකි, දර සහ ජෛව ස්කන්ධ චිප්ස් සැපයුම සඳහා මැනවින් ගැළපේ.'),
('19,129 standing trees', 'සිටුවා ඇති ගස් 19,129ක්'),
('6,943 standing trees', 'සිටුවා ඇති ගස් 6,943ක්'),
('<span>~98,000 m³ available</span>', '<span>ම³ 98,000ක් පමණ</span>'),
('<span>Sold by the tonne</span>', '<span>ටොන් ගණනින් විකිණේ</span>'),
('<span>Tea factory, bakery &amp; kiln fuel</span>', '<span>තේ කර්මාන්තශාලා, බේකරි සහ උදුන් ඉන්ධන</span>'),
('>Quote firewood</a>', '>දර සඳහා මිල ගණන්</a>'),
('Line 02 · Logs &amp; milled timber', 'පෙළ 02 · ලී කොට සහ ඉරන ලද ලී'),
('Timber Logs &amp; Sawn Timber', 'ලී කොට සහ ඉරන ලද ලී'),
('326 trees · Madampe Estate', 'ගස් 326ක් · මාදම්පේ වත්ත'),
('250 standing trees', 'සිටුවා ඇති ගස් 250ක්'),
('Estate-grown mahogany sawlogs — prized for furniture, joinery, and fine interior work.',
 'වතුවල වගා කළ මහෝගනී ලී කොට — ගෘහ භාණ්ඩ, දොර ජනෙල් සහ අභ්‍යන්තර සැරසිලි සඳහා අගය කෙරේ.'),
('Straight, tall-boled grandis for structural sawn timber and planking.',
 'ව්‍යුහාත්මක ඉරන ලද ලී සහ ලෑලි සඳහා සෘජු, උස කඳන් සහිත ග්‍රැන්ඩිස්.'),
('<span>Logs or milled to order</span>', '<span>ලී කොට හෝ ඇණවුමට ඉරා</span>'),
('<span>Furniture &amp; joinery grade</span>', '<span>ගෘහ භාණ්ඩ හා දොර ජනෙල් ශ්‍රේණියේ</span>'),
('<span>Structural planking</span>', '<span>ව්‍යුහාත්මක ලෑලි</span>'),
('>Quote timber logs</a>', '>ලී කොට සඳහා මිල ගණන්</a>'),

# ---- guide strip
('>Buyer\'s guide<', '>ගැනුම්කරු සඳහා මාර්ගෝපදේශය<'),
('Why we build our fuelwood business around Acacia mangium',
 'අපගේ දර ව්‍යාපාරය ඇකේෂියා මැංජියම් වටා ගොඩනඟන්නේ ඇයි'),
('Calorific value, ash content and seasoning compared across the fuelwood species commonly burnt in Sri Lanka.',
 'ශ්‍රී ලංකාවේ බහුලව දහනය කරන දර විශේෂ අතර තාප අගය, අළු ප්‍රමාණය සහ වියළීම සංසන්දනය කිරීම.'),
('>Read the guide →</span>', '>මාර්ගෝපදේශය කියවන්න →</span>'),

# ---- capacity
('>Resource base<', '>සම්පත් පදනම<'),
('Plantation-scale capacity', 'වතු පරිමාණයේ ධාරිතාව'),
('>Estates</div>', '>වතු</div>'),
('>Standing trees</div>', '>සිටුවා ඇති ගස්</div>'),
('>Metric tonnes</div>', '>මෙට්‍රික් ටොන්</div>'),
('>m³ standing volume</div>', '>ම³ දැව ධාරිතාව</div>'),

# ---- gallery
('>From the estates<', '>වතුයායවලින්<'),
('Timber on the ground', 'භූමියේ දැව'),
('Standing stock, harvest, and haulage across our six estates.',
 'අපගේ වතු හය පුරා සිටුවා ඇති දැව, අස්වනු නෙළීම සහ ප්‍රවාහනය.'),

# ---- logistics
('>Delivery &amp; logistics<', '>බෙදාහැරීම හා ප්‍රවාහනය<'),
('Delivered anywhere in Sri Lanka', 'ශ්‍රී ලංකාවේ ඕනෑම තැනකට බෙදාහැරේ'),
('From our Ratnapura depots to your factory, mill or yard — by the load or on standing contract. Collection ex-depot is welcome, and export shipments can be arranged on request.',
 'අපගේ රත්නපුර ගබඩාවලින් ඔබේ කර්මාන්තශාලාව, වඩු කර්මාන්තශාලාව හෝ ගබඩාව දක්වා — ලොරි පැටවීම් වශයෙන් හෝ ස්ථිර ගිවිසුමක් යටතේ. ගබඩාවෙන් ඔබම රැගෙන යාම ද පිළිගනිමු, අපනයන නැව්ගත කිරීම් ඉල්ලීම මත සකස් කළ හැක.'),
('>Harvest &amp; enumeration</h4>', '>අස්වනු නෙළීම හා ගණන් කිරීම</h4>'),
('Felling under estate supervision, with tree-by-tree enumeration records kept for your consignment.',
 'වතුයාය අධීක්ෂණය යටතේ කැපීම, ඔබේ තොගය සඳහා ගසින් ගස ගණන් කිරීමේ වාර්තා තබා ගනිමින්.'),
('>Depot &amp; weighbridge</h4>', '>ගබඩාව සහ කිරුම් පාලම</h4>'),
('Logs hauled to roadside depots; firewood weighed over certified weighbridges and sold by the metric tonne.',
 'ලී කොට මාර්ග අයිනේ ගබඩාවලට ගෙන එනු ලැබේ; දර සහතික කළ කිරුම් පාලම් මත කිරා මෙට්‍රික් ටොන් ගණනින් විකුණනු ලැබේ.'),
('>Haulage to your site</h4>', '>ඔබේ ස්ථානයට ප්‍රවාහනය</h4>'),
('Delivered by truck to factories, mills, kilns and timber yards island-wide — or collect ex-depot at a lower rate.',
 'දිවයින පුරා කර්මාන්තශාලා, වඩු කර්මාන්තශාලා, උදුන් සහ ලී ගබඩා වෙත ලොරි මගින් බෙදාහරිනු ලැබේ — නැතහොත් අඩු මිලකට ගබඩාවෙන්ම රැගෙන යන්න.'),
('>Invoicing &amp; permits</h4>', '>ඉන්වොයිස් සහ බලපත්‍ර</h4>'),
('VAT invoice and timber transport permits issued with every consignment.',
 'සෑම තොගයක් සමඟම වැට් ඉන්වොයිසිය සහ දැව ප්‍රවාහන බලපත්‍ර නිකුත් කෙරේ.'),
('<strong>Delivery terms:</strong> Ex-depot is our standard basis — you collect, or we quote haulage to your location. For export, FOB Colombo and CIF to your port can be quoted on request.',
 '<strong>බෙදාහැරීමේ නියම:</strong> ගබඩාවෙන් රැගෙන යාම අපගේ සම්මත පදනමයි — ඔබ රැගෙන යන්න, නැතහොත් ඔබේ ස්ථානයට ප්‍රවාහන ගාස්තු අපි ගණන් කර දෙන්නෙමු. අපනයන සඳහා FOB කොළඹ සහ ඔබේ වරාය දක්වා CIF ඉල්ලීම මත ගණන් කළ හැක.'),
('>Also available<', '>අමතරව<'),
('>Export enquiries</h3>', '>අපනයන විමසීම්</h3>'),
('We supply overseas buyers as well. Sri Lanka sits a short shipping corridor from the South Indian timber clusters, and we handle the paperwork end to end.',
 'අපි විදේශීය ගැනුම්කරුවන්ට ද සපයමු. දකුණු ඉන්දීය දැව කලාපවලට ශ්‍රී ලංකාව ඉතා කෙටි නාවික මාර්ගයකින් සම්බන්ධ වන අතර, ලේඛන කටයුතු මුල සිට අග දක්වා අපි කරගෙන යමු.'),
('<li>FOB Colombo or CIF to your destination port</li>', '<li>FOB කොළඹ හෝ ඔබේ ගමනාන්ත වරාය දක්වා CIF</li>'),
('<li>Phytosanitary &amp; export documentation prepared</li>', '<li>ශාක සත්කාරක සහ අපනයන ලේඛන සකස් කර දෙනු ලැබේ</li>'),
('<li>Containerised or break-bulk loading</li>', '<li>කන්ටේනර් හෝ තොග වශයෙන් පැටවීම</li>'),

# ---- RFQ
('>Request a Quote</span>', '>මිල ගණන් ඉල්ලීම</span>'),
('Tell us what you need', 'ඔබට අවශ්‍ය දේ අපට කියන්න'),
('Tell us what you need and send it straight from this page — no email app required. We reply with pricing and availability, usually within one working day.',
 'ඔබට අවශ්‍ය දේ සඳහන් කර මෙම පිටුවෙන්ම කෙලින්ම එවන්න — විද්‍යුත් තැපැල් යෙදුමක් අවශ්‍ය නැත. සාමාන්‍යයෙන් වැඩ කරන දිනක් තුළ මිල ගණන් සහ තිබෙන ප්‍රමාණය සමඟ පිළිතුරු දෙන්නෙමු.'),
('Your name <span class="req">*</span>', 'ඔබේ නම <span class="req">*</span>'),
('placeholder="Your full name"', 'placeholder="ඔබේ සම්පූර්ණ නම"'),
('Company / buyer name <span class="hint">(optional)</span>', 'සමාගම / ගැනුම්කරුගේ නම <span class="hint">(අත්‍යවශ්‍ය නොවේ)</span>'),
('placeholder="e.g. tea factory, sawmill, timber yard"', 'placeholder="උදා: තේ කර්මාන්තශාලාව, වඩු කර්මාන්තශාලාව"'),
('>Country</label>', '>රට</label>'),
('>Sri Lanka</option>', '>ශ්‍රී ලංකාව</option>'),
('>India</option>', '>ඉන්දියාව</option>'),
('>Other (export)</option>', '>වෙනත් (අපනයන)</option>'),
('>City / town</label>', '>නගරය</label>'),
('placeholder="e.g. Ratnapura, Colombo, Kandy…"', 'placeholder="උදා: රත්නපුර, කොළඹ, මහනුවර…"'),
('Email <span class="req">*</span>', 'විද්‍යුත් තැපෑල <span class="req">*</span>'),
('Phone / WhatsApp <span class="hint">(with country code)</span>', 'දුරකථන / WhatsApp <span class="hint">(රට කේතය සමඟ)</span>'),
('Product line <span class="req">*</span>', 'නිෂ්පාදන පෙළ <span class="req">*</span>'),
('— Select a product line —', '— නිෂ්පාදන පෙළක් තෝරන්න —'),
('Biomass &amp; Fuelwood (by MT)', 'දර සහ ජෛව ස්කන්ධ (මෙ.ටොන් අනුව)'),
('>Sawn Timber &amp; Planks</option>', '>ඉරන ලද ලී සහ ලෑලි</option>'),
('>Both</option>', '>දෙකම</option>'),
('Species of interest <span class="hint">(tick all that apply)</span>',
 'උනන්දුවක් දක්වන විශේෂ <span class="hint">(අදාළ සියල්ල තෝරන්න)</span>'),
('>Estimated volume required</label>', '>අවශ්‍ය ආසන්න ප්‍රමාණය</label>'),
('>Containers</button>', '>කන්ටේනර්</button>'),
('Delivery terms preference <span class="hint">(Ex-depot is our default)</span>',
 'බෙදාහැරීමේ නියම <span class="hint">(ගබඩාවෙන් රැගෙන යාම සම්මතයයි)</span>'),
('> Ex-depot</label>', '> ගබඩාවෙන්</label>'),
('Delivery location <span class="hint">(or port, if exporting)</span>',
 'බෙදාහරින ස්ථානය <span class="hint">(අපනයනයේදී වරාය)</span>'),
('placeholder="e.g. factory at Avissawella, or Colombo Port"',
 'placeholder="උදා: අවිස්සාවේල්ලේ කර්මාන්තශාලාව, හෝ කොළඹ වරාය"'),
('>Target timeframe</label>', '>අපේක්ෂිත කාලසීමාව</label>'),
('placeholder="e.g. within 2 months"', 'placeholder="උදා: මාස 2ක් ඇතුළත"'),
('>Message / additional requirements</label>', '>පණිවිඩය / අමතර අවශ්‍යතා</label>'),
('placeholder="Girth/length specs, moisture limits, inspection visit, payment terms…"',
 'placeholder="වට ප්‍රමාණය/දිග, තෙතමනය, පරීක්ෂා කිරීමේ පැමිණීම, ගෙවීම් නියම…"'),
('>Send my request →</button>', '>මගේ ඉල්ලීම යවන්න →</button>'),
('We reply with pricing and availability, usually within one working day.',
 'සාමාන්‍යයෙන් වැඩ කරන දිනක් තුළ මිල ගණන් සහ තිබෙන ප්‍රමාණය සමඟ පිළිතුරු දෙන්නෙමු.'),
("Thank you — we've got your request", 'ස්තූතියි — ඔබේ ඉල්ලීම අපට ලැබී ඇත'),
("It's been sent straight to our team. We'll reply to <strong id=\"echo-email\">your email</strong> with pricing and availability, usually within one working day. Prefer to talk now? Message us on WhatsApp.",
 'එය කෙලින්ම අපගේ කණ්ඩායමට යවා ඇත. සාමාන්‍යයෙන් වැඩ කරන දිනක් තුළ <strong id="echo-email">ඔබේ විද්‍යුත් තැපෑලට</strong> මිල ගණන් සමඟ පිළිතුරු දෙන්නෙමු. දැන්ම කතා කිරීමට කැමතිද? WhatsApp හරහා අපට පණිවිඩයක් යවන්න.'),
('Your request is ready to send', 'ඔබේ ඉල්ලීම යැවීමට සූදානම්'),
("Choose how you'd like to send it — your email app or WhatsApp will open with the full request already written. Just press send.",
 'එය යවන ආකාරය තෝරන්න — ඔබේ විද්‍යුත් තැපැල් යෙදුම හෝ WhatsApp සම්පූර්ණ ඉල්ලීම සමඟ විවෘත වේ. යවන්න ඔබන්න පමණයි.'),
('Send by Email', 'විද්‍යුත් තැපෑලෙන් යවන්න'),
('Send by WhatsApp', 'WhatsApp හරහා යවන්න'),
('← Edit or start a new request', '← සංස්කරණය කරන්න හෝ අලුත් ඉල්ලීමක්'),

# ---- contact
('>Contact</span>', '>සම්බන්ධතා</span>'),
('Speak to us directly', 'අප හා කෙලින්ම කතා කරන්න'),
('Buyers are welcome to inspect standing timber on the estates by appointment.',
 'පෙර හමුවීමක් ලබාගෙන වතුයායවල සිටුවා ඇති දැව පරීක්ෂා කිරීමට ගැනුම්කරුවන්ට ආරාධනා කරමු.'),
('>Phone / WhatsApp</h4>', '>දුරකථන / WhatsApp</h4>'),
('WhatsApp available — English, සිංහල &amp; தமிழ் enquiries welcome',
 'WhatsApp තිබේ — සිංහල, English සහ தமிழ் විමසීම් පිළිගනිමු'),
('>Email</h4>', '>විද්‍යුත් තැපෑල</h4>'),
('>Office</h4>', '>කාර්යාලය</h4>'),
('31 Layards Road, Colombo 05, Sri Lanka', '31 ලයාඩ්ස් පාර, කොළඹ 05, ශ්‍රී ලංකාව'),
('Estates: Ratnapura District, Sabaragamuwa Province', 'වතු: රත්නපුර දිස්ත්‍රික්කය, සබරගමුව පළාත'),
('>Hours</h4>', '>වේලාවන්</h4>'),
('Mon–Sat, 8:00–18:00 Sri Lanka Standard Time (UTC+5:30)',
 'සඳුදා–සෙනසුරාදා, පෙ.ව 8:00–ප.ව 6:00 ශ්‍රී ලංකා වේලාව (UTC+5:30)'),

# ---- footer / sticky
('VAT-registered plantation timber company · Timber rights via Browns Group / Hapugastenne Plantations PLC',
 'වැට් ලියාපදිංචි වතු දැව සමාගමකි · දැව අයිතිය බ්‍රවුන්ස් සමූහය / හපුගස්තැන්න ප්ලාන්ටේෂන්ස් PLC හරහා'),
('All rights reserved.', 'සියලු හිමිකම් ඇවිරිණි.'),
('>Request a Quote →</a>', '>මිල ගණන් ඉල්ලන්න →</a>'),
('>Skip intro →</button>', '>හැඳින්වීම මඟහරින්න →</button>'),

# ---- validation messages
('Please enter your name.', 'කරුණාකර ඔබේ නම ඇතුළත් කරන්න.'),
('Please enter a valid email address.', 'කරුණාකර වලංගු විද්‍යුත් තැපැල් ලිපිනයක් ඇතුළත් කරන්න.'),
('Please choose a product line.', 'කරුණාකර නිෂ්පාදන පෙළක් තෝරන්න.'),
('Sending your request…', 'ඔබේ ඉල්ලීම යවමින්…'),
('sendBtn.textContent = "Sending…"', 'sendBtn.textContent = "යවමින්…"'),
]

out = src
missing = []
# longest source strings first: stops a short heading clobbering a longer
# sentence that happens to contain it
for en, si in sorted(T, key=lambda x: -len(x[0])):
    if en in out:
        out = out.replace(en, si)
    else:
        missing.append(en[:60])

# ---- page-level changes -------------------------------------------------
out = out.replace('<html lang="en">', '<html lang="si">', 1)
out = out.replace(
    '<title>Timber &amp; Firewood Supplier Sri Lanka | Shenron Timber</title>',
    '<title>ශ්‍රී ලංකාවේ දර හා දැව සැපයුම්කරු | ෂෙන්රොන් ටිම්බර්</title>', 1)
out = re.sub(r'<meta name="description" content="[^"]*">',
    '<meta name="description" content="රත්නපුර වතු හයකින් වතුවල වගා කළ දර, ජෛව ස්කන්ධ ලී කොට සහ දැව මිලදී ගන්න. දිවයින පුරා බෙදාහැරීම, ප්‍රවාහන බලපත්‍ර, වැට් ඉන්වොයිස් සහ අපනයන පහසුකම්.">',
    out, count=1)
# index.html already carries the hreflang set; only the canonical differs
out = out.replace('<link rel="canonical" href="https://shenrontimber.com/">',
                  '<link rel="canonical" href="https://shenrontimber.com/si/">', 1)
out = out.replace('<meta property="og:url" content="https://shenrontimber.com/">',
                  '<meta property="og:url" content="https://shenrontimber.com/si/">', 1)
out = out.replace('"inLanguage": "en"', '"inLanguage": "si"', 1)
# strip the search-console tag (belongs on one page only) and the site's intro block src
out = re.sub(r'<meta name="google-site-verification"[^>]*>\n', '', out, count=1)
# index.html uses paths relative to the site root; /si/ is one level down
out = out.replace('href="assets/site.css"', 'href="../assets/site.css"')
out = out.replace('href="articles/acacia-mangium-fuelwood/"', 'href="../articles/acacia-mangium-fuelwood/"')
out = out.replace('href="articles/"', 'href="../articles/"')
out = out.replace('href="si/"', 'href="../"')          # language link -> English
out = out.replace('SRC = "assets/intro.mp4"', 'SRC = "../assets/intro.mp4"')
out = out.replace('src="images/', 'src="../images/')

# language switch points back to English from the Sinhala page
out = re.sub(r'<a class="lang-link" href="\.\./" hreflang="si" lang="si">[^<]*</a>',
             '<a class="lang-link" href="../" hreflang="en" lang="en">English</a>', out)
out = out.replace('var LANG_PAGE = "en";                 // this file is the English page',
                  'var LANG_PAGE = "si";                 // this file is the Sinhala page')
# on the Sinhala page the bar\'s English option is the link, Sinhala the button
out = re.sub(r'<a href="si/" hreflang="si" lang="si" data-lang="si">[^<]*</a>\s*<button type="button" data-lang="en">English</button>',
             '<button type="button" data-lang="si" lang="si">\u0dc3\u0dd2\u0d82\u0dc4\u0dbd</button>\n    <a href="../" hreflang="en" lang="en" data-lang="en">English</a>', out)
out = out.replace('if (v !== "si") { e.preventDefault(); bar.classList.remove("show"); }',
                  'if (v !== "en") { e.preventDefault(); bar.classList.remove("show"); }')

(ROOT / "si").mkdir(exist_ok=True)
(ROOT / "si" / "index.html").write_text(out)
print("wrote si/index.html")
print("translations applied:", len(T) - len(missing), "/", len(T))
if missing:
    print("NOT FOUND (check these):")
    for m in missing: print("   ", m)
