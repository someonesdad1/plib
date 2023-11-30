'''
Print out URIs (Uniform Resource Identifier schemes)

The fields are

    0   URI Scheme
    1   Template
    2   Description
    3   Status
    4   Well-Known URI Support
    5   Reference
    6   Notes

Status elements are Permanent, Provisional, or Historical.  The script
prints out the URIs of each status.
'''
import csv
from io import StringIO
from columnize import Columnize

# Web page:  https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml
# For the data, use the link to the CSV file
# https://www.iana.org/assignments/uri-schemes/uri-schemes-1.csv
data = '''
URI Scheme,Template,Description,Status,Well-Known URI Support,Reference,Notes
aaa,,Diameter Protocol,Permanent,-,[RFC6733],
aaas,,Diameter Protocol with Secure Transport,Permanent,-,[RFC6733],
about,,about,Permanent,-,[RFC6694],
acap,,application configuration access protocol,Permanent,-,[RFC2244],
acct,,acct,Permanent,-,[RFC7565],
acd,prov/acd,acd,Provisional,-,[Michael_Hedenus],
acr,prov/acr,acr,Provisional,-,[OMA-OMNA],
adiumxtra,prov/adiumxtra,adiumxtra,Provisional,-,[Dave_Thaler],
adt,prov/adt,adt,Provisional,-,[SAP_SE],
afp,prov/afp,afp,Provisional,-,[Dave_Thaler],
afs,,Andrew File System global file names,Provisional,-,[RFC1738],
aim,prov/aim,aim,Provisional,-,[Dave_Thaler],
amss,prov/amss,amss,Provisional,-,[RadioDNS_Project],
android,prov/android,android,Provisional,-,[Adam_Barth][https://developer.android.com/guide/topics/manifest/manifest-intro],
appdata,prov/appdata,appdata,Provisional,-,[urischemeowners_at_microsoft.com],
apt,prov/apt,apt,Provisional,-,[Dave_Thaler],
ar,prov/ar,ar,Provisional,-,[Arweave_Team],
ark,prov/ark,ark,Provisional,-,[ARK_agency][https://n2t.net/ark:/21206/10015],
at,prov/at,at (see [reviewer notes]),Provisional,-,[Bluesky_PBLLC][Paul_Frazee],
attachment,prov/attachment,attachment,Provisional,-,[Dave_Thaler],
aw,prov/aw,aw,Provisional,-,[Dave_Thaler],
barion,prov/barion,barion,Provisional,-,[Bíró_Tamás],
bb,historic/bb,bb,Historical,-,[IESG],
beshare,prov/beshare,beshare,Provisional,-,[Dave_Thaler],
bitcoin,prov/bitcoin,bitcoin,Provisional,-,[Dave_Thaler],
bitcoincash,prov/bitcoincash,bitcoincash,Provisional,-,[Corentin_Mercier],
blob,prov/blob,blob,Provisional,-,[W3C_WebApps_Working_Group][Chris_Rebert],
bolo,prov/bolo,bolo,Provisional,-,[Dave_Thaler],
brid,prov/brid,brid,Provisional,-,[Jürgen_Grupp][Michael_Ranft][Sophie_Schenkel],
browserext,prov/browserext,browserext,Provisional,-,[Mike_Pietraszak],
cabal,prov/cabal,cabal,Provisional,-,[Frédéric_Wang][Cabal_Club],
calculator,prov/calculator,calculator,Provisional,-,[urischemeowners_at_microsoft.com],
callto,prov/callto,callto,Provisional,-,[Alexey_Melnikov],
cap,,Calendar Access Protocol,Permanent,-,[RFC4324],
cast,prov/cast,cast,Provisional,-,[Adam_Barth][https://developers.google.com/cast/docs/registration],
casts,prov/casts,casts,Provisional,-,[Adam_Barth][https://developers.google.com/cast/docs/registration],
chrome,prov/chrome,chrome,Provisional,-,[Dave_Thaler],
chrome-extension,prov/chrome-extension,chrome-extension,Provisional,-,[Dave_Thaler],
cid,,content identifier,Permanent,-,[RFC2392],
coap,,coap,Permanent,[RFC7252],[RFC7252],
coap+tcp,,coap+tcp (see [reviewer notes]),Permanent,[RFC8323],[RFC8323],
coap+ws,,coap+ws (see [reviewer notes]),Permanent,[RFC8323],[RFC8323],
coaps,,coaps,Permanent,[RFC7252],[RFC7252],
coaps+tcp,,coaps+tcp (see [reviewer notes]),Permanent,[RFC8323],[RFC8323],
coaps+ws,,coaps+ws (see [reviewer notes]),Permanent,[RFC8323],[RFC8323],
com-eventbrite-attendee,prov/com-eventbrite-attendee,com-eventbrite-attendee,Provisional,-,[Bob_Van_Zant],
content,prov/content,content,Provisional,-,[Dave_Thaler],
content-type,prov/content-type,content-type,Provisional,-,[Donald_Eastlake],
crid,,TV-Anytime Content Reference Identifier,Permanent,-,[RFC4078],
cstr,prov/cstr,cstr,Provisional,-,[Wang_Shu],
cvs,prov/cvs,cvs,Provisional,-,[Dave_Thaler],
dab,prov/dab,dab,Provisional,-,[RadioDNS_Project],
dat,prov/dat,dat,Provisional,-,[Frédéric_Wang][Paul_Frazee],
data,,data,Permanent,-,[RFC2397],
dav,,dav,Permanent,-,[RFC4918],
dhttp,prov/dhttp,dhttp (see [reviewer notes]),Provisional,-,[Qi_Zhou],
diaspora,prov/diaspora,diaspora,Provisional,-,[Dennis_Schubert],
dict,,dictionary service protocol,Permanent,-,[RFC2229],
did,prov/did,did,Provisional,-,[W3C_Decentralized_Identifier_Working_Group][Manu_Sporny][Ivan_Herman],
dis,prov/dis,dis,Provisional,-,[Christophe_Meessen],
dlna-playcontainer,prov/dlna-playcontainer,dlna-playcontainer,Provisional,-,[DLNA],
dlna-playsingle,prov/dlna-playsingle,dlna-playsingle,Provisional,-,[DLNA],
dns,,Domain Name System,Permanent,-,[RFC4501],
dntp,prov/dntp,dntp,Provisional,-,[Hans-Dieter_A._Hiep],
doi,prov/doi,doi,Provisional,-,[Frédéric_Wang][International_DOI_Foundation],
dpp,prov/dpp,dpp,Provisional,-,[Gaurav_Jain][Wi-Fi_Alliance],
drm,prov/drm,drm,Provisional,-,[RadioDNS_Project],
drop,historic/drop,drop,Historical,-,[IESG],
dtmi,prov/dtmi,dtmi,Provisional,-,[urischemeowners_at_microsoft.com],
dtn,,DTNRG research and development,Permanent,-,[RFC9171],
dvb,,dvb,Provisional,-,[draft-mcroberts-uri-dvb],
dvx,prov/dvx,dvx,Provisional,-,[Clemens_Bastian],
dweb,prov/dweb,dweb,Provisional,-,[Frédéric_Wang][Protocol_Labs],
ed2k,prov/ed2k,ed2k,Provisional,-,[Dave_Thaler],
eid,prov/eid,eid,Provisional,-,[eSIM_Group_GSM_Association],
elsi,prov/elsi,elsi,Provisional,-,[Kimmo_Lindholm],
embedded,prov/embedded,embedded,Provisional,-,[Peter_Hoddie],
ens,prov/ens,ens,Provisional,-,[Ricky_Bloomfield][Bradley_Nelson],
ethereum,prov/ethereum,ethereum,Provisional,-,[Frédéric_Wang][ligi],
example,,example,Permanent,-,[RFC7595],
facetime,prov/facetime,facetime,Provisional,-,[Dave_Thaler],
fax,,fax,Historical,-,[RFC2806][RFC3966],
feed,prov/feed,feed,Provisional,-,[Dave_Thaler],
feedready,prov/feedready,feedready,Provisional,-,[Mirko_Nosenzo],
fido,prov/fido,fido,Provisional,-,[Adam_Langley],
file,,Host-specific file names,Permanent,-,[RFC8089],
filesystem,historic/filesystem,filesystem,Historical,-,[W3C_WebApps_Working_Group][Chris_Rebert],
finger,prov/finger,finger,Provisional,-,[Dave_Thaler],
first-run-pen-experience,prov/first-run-pen-experience,first-run-pen-experience,Provisional,-,[urischemeowners_at_microsoft.com],
fish,prov/fish,fish,Provisional,-,[Dave_Thaler],
fm,prov/fm,fm,Provisional,-,[RadioDNS_Project],
ftp,,File Transfer Protocol,Permanent,-,[RFC1738],
fuchsia-pkg,prov/fuchsia-pkg,fuchsia-pkg,Provisional,-,[Adam_Barth][https://fuchsia.googlesource.com/fuchsia/],
geo,,Geographic Locations,Permanent,-,[RFC5870],
gg,prov/gg,gg,Provisional,-,[Dave_Thaler],
git,prov/git,git,Provisional,-,[Dave_Thaler],
gitoid,prov/gitoid,gitoid,Provisional,-,[Ed_Warnicke],
gizmoproject,prov/gizmoproject,gizmoproject,Provisional,-,[Dave_Thaler],
go,,go,Permanent,-,[RFC3368],
gopher,,The Gopher Protocol,Permanent,-,[RFC4266],
graph,prov/graph,graph,Provisional,-,[Alastair_Green],
grd,historic/grd,grd,Historical,-,[IESG],
gtalk,prov/gtalk,gtalk,Provisional,-,[Dave_Thaler],
h323,,H.323,Permanent,-,[RFC3508],
ham,,ham,Provisional,-,[RFC7046],
hcap,prov/hcap,hcap,Provisional,-,[urischemeowners_at_microsoft.com],
hcp,prov/hcp,hcp,Provisional,-,[Alexey_Melnikov],
http,,Hypertext Transfer Protocol,Permanent,[RFC8615],"[RFC9110, Section 4.2.1]",
https,,Hypertext Transfer Protocol Secure,Permanent,[RFC8615],"[RFC9110, Section 4.2.2]",
hxxp,prov/hxxp,hxxp,Provisional,-,[draft-salgado-hxxp],
hxxps,prov/hxxps,hxxps,Provisional,-,[draft-salgado-hxxp],
hydrazone,prov/hydrazone,hydrazone,Provisional,-,[Matthias_Merkel][https://tech.hydrazone.pro/uri/specification/hydrazone.txt],
hyper,prov/hyper,hyper,Provisional,-,[Frédéric_Wang][Paul_Frazee],
iax,,Inter-Asterisk eXchange Version 2,Permanent,-,[RFC5456],
icap,,Internet Content Adaptation Protocol,Permanent,-,[RFC3507],
icon,,icon,Provisional,-,[draft-lafayette-icon-uri-scheme],
im,,Instant Messaging,Permanent,-,[RFC3860],
imap,,internet message access protocol,Permanent,-,[RFC5092],
info,,"Information Assets with Identifiers in Public Namespaces. [RFC4452] (section 3) defines an ""info"" registry of public namespaces, which is maintained by NISO and can be accessed from [http://info-uri.info/].",Permanent,-,[RFC4452],
iotdisco,prov/iotdisco,iotdisco,Provisional,-,[Peter_Waher][https://www.iana.org/assignments/uri-schemes/prov/iotdisco.pdf],
ipfs,prov/ipfs,ipfs,Provisional,-,[Frédéric_Wang][Protocol_Labs],
ipn,,ipn,Permanent,-,[RFC9171],
ipns,prov/ipns,ipns,Provisional,-,[Frédéric_Wang][Protocol_Labs],
ipp,,Internet Printing Protocol,Permanent,-,[RFC3510],
ipps,,Internet Printing Protocol over HTTPS,Permanent,-,[RFC7472],
irc,prov/irc,irc,Provisional,-,[Dave_Thaler],
irc6,prov/irc6,irc6,Provisional,-,[Dave_Thaler],
ircs,prov/ircs,ircs,Provisional,-,[Dave_Thaler],
iris,,Internet Registry Information Service,Permanent,-,[RFC3981],
iris.beep,,iris.beep,Permanent,-,[RFC3983],
iris.lwz,,iris.lwz,Permanent,-,[RFC4993],
iris.xpc,,iris.xpc,Permanent,-,[RFC4992],
iris.xpcs,,iris.xpcs,Permanent,-,[RFC4992],
isostore,prov/isostore,isostore,Provisional,-,[urischemeowners_at_microsoft.com],
itms,prov/itms,itms,Provisional,-,[Dave_Thaler],
jabber,perm/jabber,jabber,Permanent,-,[Peter_Saint-Andre],
jar,prov/jar,jar,Provisional,-,[Dave_Thaler],
jms,,Java Message Service,Provisional,-,[RFC6167],
keyparc,prov/keyparc,keyparc,Provisional,-,[Dave_Thaler],
lastfm,prov/lastfm,lastfm,Provisional,-,[Dave_Thaler],
lbry,prov/lbry,lbry,Provisional,-,[Alex_Grintsvayg],
ldap,,Lightweight Directory Access Protocol,Permanent,-,[RFC4516],
ldaps,prov/ldaps,ldaps,Provisional,-,[Dave_Thaler],
leaptofrogans,,leaptofrogans,Permanent,-,[RFC8589],
lid,prov/lid,lid,Provisional,-,[IS4],
lorawan,prov/lorawan,lorawan,Provisional,-,[OMA-DMSE],
lpa,prov/lpa,lpa,Provisional,-,[eSIM_Group_GSM_Association],
lvlt,prov/lvlt,lvlt,Provisional,-,[Alexander_Shishenko],
magnet,prov/magnet,magnet,Provisional,-,[Dave_Thaler],
mailserver,,Access to data available from mail servers,Historical,-,[RFC6196],
mailto,,Electronic mail address,Permanent,-,[RFC6068],
maps,prov/maps,maps,Provisional,-,[Dave_Thaler],
market,prov/market,market,Provisional,-,[Dave_Thaler],
matrix,prov/matrix,matrix,Provisional,-,[Hubert_Chathi],
message,prov/message,message,Provisional,-,[Dave_Thaler],
microsoft.windows.camera,prov/microsoft.windows.camera,microsoft.windows.camera,Provisional,-,[urischemeowners_at_microsoft.com],
microsoft.windows.camera.multipicker,prov/microsoft.windows.camera.multipicker,microsoft.windows.camera.multipicker,Provisional,-,[urischemeowners_at_microsoft.com],
microsoft.windows.camera.picker,prov/microsoft.windows.camera.picker,microsoft.windows.camera.picker,Provisional,-,[urischemeowners_at_microsoft.com],
mid,,message identifier,Permanent,-,[RFC2392],
mms,prov/mms,mms,Provisional,-,[Alexey_Melnikov],
modem,,modem,Historical,-,[RFC2806][RFC3966],
mongodb,prov/mongodb,mongodb,Provisional,-,[Ignacio_Losiggio][Mongo_DB_Inc],
moz,prov/moz,moz,Provisional,-,[Joe_Hildebrand],
ms-access,prov/ms-access,ms-access,Provisional,-,[urischemeowners_at_microsoft.com],
ms-appinstaller,prov/ms-appinstaller,ms-appinstaller,Provisional,-,[urischemeowners_at_microsoft.com],
ms-browser-extension,prov/ms-browser-extension,ms-browser-extension,Provisional,-,[urischemeowners_at_microsoft.com],
ms-calculator,prov/ms-calculator,ms-calculator,Provisional,-,[urischemeowners_at_microsoft.com],
ms-drive-to,prov/ms-drive-to,ms-drive-to,Provisional,-,[urischemeowners_at_microsoft.com],
ms-enrollment,prov/ms-enrollment,ms-enrollment,Provisional,-,[urischemeowners_at_microsoft.com],
ms-excel,prov/ms-excel,ms-excel,Provisional,-,[urischemeowners_at_microsoft.com],
ms-eyecontrolspeech,prov/ms-eyecontrolspeech,ms-eyecontrolspeech,Provisional,-,[urischemeowners_at_microsoft.com],
ms-gamebarservices,prov/ms-gamebarservices,ms-gamebarservices,Provisional,-,[urischemeowners_at_microsoft.com],
ms-gamingoverlay,prov/ms-gamingoverlay,ms-gamingoverlay,Provisional,-,[urischemeowners_at_microsoft.com],
ms-getoffice,prov/ms-getoffice,ms-getoffice,Provisional,-,[urischemeowners_at_microsoft.com],
ms-help,prov/ms-help,ms-help,Provisional,-,[Alexey_Melnikov],
ms-infopath,prov/ms-infopath,ms-infopath,Provisional,-,[urischemeowners_at_microsoft.com],
ms-inputapp,prov/ms-inputapp,ms-inputapp,Provisional,-,[urischemeowners_at_microsoft.com],
ms-launchremotedesktop,prov/ms-launchremotedesktop,ms-launchremotedesktop,Provisional,-,[urischemeowners_at_microsoft.com],
ms-lockscreencomponent-config,prov/ms-lockscreencomponent-config,ms-lockscreencomponent-config,Provisional,-,[urischemeowners_at_microsoft.com],
ms-media-stream-id,prov/ms-media-stream-id,ms-media-stream-id,Provisional,-,[urischemeowners_at_microsoft.com],
ms-meetnow,prov/ms-meetnow,ms-meetnow,Provisional,-,[urischemeowners_at_microsoft.com],
ms-mixedrealitycapture,prov/ms-mixedrealitycapture,ms-mixedrealitycapture,Provisional,-,[urischemeowners_at_microsoft.com],
ms-mobileplans,prov/ms-mobileplans,ms-mobileplans,Provisional,-,[urischemeowners_at_microsoft.com],
ms-newsandinterests,prov/ms-newsandinterests,ms-newsandinterests,Provisional,-,[urischemeowners_at_microsoft.com],
ms-officeapp,prov/ms-officeapp,ms-officeapp,Provisional,-,[urischemeowners_at_microsoft.com],
ms-people,prov/ms-people,ms-people,Provisional,-,[urischemeowners_at_microsoft.com],
ms-project,prov/ms-project,ms-project,Provisional,-,[urischemeowners_at_microsoft.com],
ms-powerpoint,prov/ms-powerpoint,ms-powerpoint,Provisional,-,[urischemeowners_at_microsoft.com],
ms-publisher,prov/ms-publisher,ms-publisher,Provisional,-,[urischemeowners_at_microsoft.com],
ms-remotedesktop,prov/ms-remotedesktop,ms-remotedesktop,Provisional,-,[urischemeowners_at_microsoft.com],
ms-remotedesktop-launch,prov/ms-remotedesktop-launch,ms-remotedesktop-launch,Provisional,-,[urischemeowners_at_microsoft.com],
ms-restoretabcompanion,prov/ms-restoretabcompanion,ms-restoretabcompanion,Provisional,-,[urischemeowners_at_microsoft.com],
ms-screenclip,prov/ms-screenclip,ms-screenclip,Provisional,-,[urischemeowners_at_microsoft.com],
ms-screensketch,prov/ms-screensketch,ms-screensketch,Provisional,-,[urischemeowners_at_microsoft.com],
ms-search,prov/ms-search,ms-search,Provisional,-,[urischemeowners_at_microsoft.com],
ms-search-repair,prov/ms-search-repair,ms-search-repair,Provisional,-,[urischemeowners_at_microsoft.com],
ms-secondary-screen-controller,prov/ms-secondary-screen-controller,ms-secondary-screen-controller,Provisional,-,[urischemeowners_at_microsoft.com],
ms-secondary-screen-setup,prov/ms-secondary-screen-setup,ms-secondary-screen-setup,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings,prov/ms-settings,ms-settings,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-airplanemode,prov/ms-settings-airplanemode,ms-settings-airplanemode,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-bluetooth,prov/ms-settings-bluetooth,ms-settings-bluetooth,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-camera,prov/ms-settings-camera,ms-settings-camera,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-cellular,prov/ms-settings-cellular,ms-settings-cellular,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-cloudstorage,prov/ms-settings-cloudstorage,ms-settings-cloudstorage,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-connectabledevices,prov/ms-settings-connectabledevices,ms-settings-connectabledevices,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-displays-topology,prov/ms-settings-displays-topology,ms-settings-displays-topology,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-emailandaccounts,prov/ms-settings-emailandaccounts,ms-settings-emailandaccounts,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-language,prov/ms-settings-language,ms-settings-language,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-location,prov/ms-settings-location,ms-settings-location,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-lock,prov/ms-settings-lock,ms-settings-lock,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-nfctransactions,prov/ms-settings-nfctransactions,ms-settings-nfctransactions,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-notifications,prov/ms-settings-notifications,ms-settings-notifications,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-power,prov/ms-settings-power,ms-settings-power,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-privacy,prov/ms-settings-privacy,ms-settings-privacy,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-proximity,prov/ms-settings-proximity,ms-settings-proximity,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-screenrotation,prov/ms-settings-screenrotation,ms-settings-screenrotation,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-wifi,prov/ms-settings-wifi,ms-settings-wifi,Provisional,-,[urischemeowners_at_microsoft.com],
ms-settings-workplace,prov/ms-settings-workplace,ms-settings-workplace,Provisional,-,[urischemeowners_at_microsoft.com],
ms-spd,prov/ms-spd,ms-spd,Provisional,-,[urischemeowners_at_microsoft.com],
ms-stickers,prov/ms-stickers,ms-stickers,Provisional,-,[urischemeowners_at_microsoft.com],
ms-sttoverlay,prov/ms-sttoverlay,ms-sttoverlay,Provisional,-,[urischemeowners_at_microsoft.com],
ms-transit-to,prov/ms-transit-to,ms-transit-to,Provisional,-,[urischemeowners_at_microsoft.com],
ms-useractivityset,prov/ms-useractivityset,ms-useractivityset,Provisional,-,[urischemeowners_at_microsoft.com],
ms-virtualtouchpad,prov/ms-virtualtouchpad,ms-virtualtouchpad,Provisional,-,[urischemeowners_at_microsoft.com],
ms-visio,prov/ms-visio,ms-visio,Provisional,-,[urischemeowners_at_microsoft.com],
ms-walk-to,prov/ms-walk-to,ms-walk-to,Provisional,-,[urischemeowners_at_microsoft.com],
ms-whiteboard,prov/ms-whiteboard,ms-whiteboard,Provisional,-,[urischemeowners_at_microsoft.com],
ms-whiteboard-cmd,prov/ms-whiteboard-cmd,ms-whiteboard-cmd,Provisional,-,[urischemeowners_at_microsoft.com],
ms-word,prov/ms-word,ms-word,Provisional,-,[urischemeowners_at_microsoft.com],
msnim,prov/msnim,msnim,Provisional,-,[Alexey_Melnikov],
msrp,,Message Session Relay Protocol,Permanent,-,[RFC4975],
msrps,,Message Session Relay Protocol Secure,Permanent,-,[RFC4975][RFC8873],
mss,prov/mss,mss,Provisional,-,[Jarmo_Miettinen],
mt,perm/mt,Matter protocol on-boarding payloads that are encoded for use in QR Codes and/or NFC Tags,Permanent,-,[Connectivity_Standards_Alliance],
mtqp,,Message Tracking Query Protocol,Permanent,-,[RFC3887],
mumble,prov/mumble,mumble,Provisional,-,[Dave_Thaler],
mupdate,,Mailbox Update (MUPDATE) Protocol,Permanent,-,[RFC3656],
mvn,prov/mvn,mvn,Provisional,-,[Dave_Thaler],
news,,USENET news,Permanent,-,[RFC5538],
nfs,,network file system protocol,Permanent,-,[RFC2224],
ni,,ni,Permanent,-,[RFC6920],
nih,,nih,Permanent,-,[RFC6920],
nntp,,USENET news using NNTP access,Permanent,-,[RFC5538],
notes,prov/notes,notes,Provisional,-,[draft-dconmy-notes-uri-scheme-02],
num,prov/num,Namespace Utility Modules,Provisional,-,[Elliott_Brown][https://www.numprotocol.com/specification],
ocf,prov/ocf,ocf,Provisional,-,[Dave_Thaler],
oid,prov/oid,oid,Provisional,-,[draft-larmouth-oid-iri],
onenote,prov/onenote,onenote,Provisional,-,[urischemeowners_at_microsoft.com],
onenote-cmd,prov/onenote-cmd,onenote-cmd,Provisional,-,[urischemeowners_at_microsoft.com],
opaquelocktoken,,opaquelocktokent,Permanent,-,[RFC4918],
openid,prov/openid,OpenID Connect,Provisional,-,"[OpenID_Foundation_Artifact_Binding_Working_Group][OpenID Connect Core 1.0, Section 7.3]",
openpgp4fpr,prov/openpgp4fpr,openpgp4fpr,Provisional,-,[Wiktor_Kwapisiewicz],
otpauth,prov/otpauth,otpauth,Provisional,-,[Frédéric_Wang][Thomas_Habets],
p1,historic/p1,p1,Historical,-,[IESG],
pack,historic/pack,pack,Historical,-,[draft-shur-pack-uri-scheme],
palm,prov/palm,palm,Provisional,-,[Dave_Thaler],
paparazzi,prov/paparazzi,paparazzi,Provisional,-,[Dave_Thaler],
payment,prov/payment,payment,Provisional,-,[Arild_Hegvik][https://bitcoincheque.org],
payto,prov/payto,payto,Provisional,-,[RFC8905],
pkcs11,,PKCS#11,Permanent,-,[RFC7512],
platform,prov/platform,platform,Provisional,-,[Dave_Thaler],
pop,,Post Office Protocol v3,Permanent,-,[RFC2384],
pres,,Presence,Permanent,-,[RFC3859],
prospero,,Prospero Directory Service,Historical,-,[RFC4157],
proxy,prov/proxy,proxy,Provisional,-,[Dave_Thaler],
pwid,prov/pwid,pwid,Provisional,-,[Eld_Zierau],
psyc,prov/psyc,psyc,Provisional,-,[Dave_Thaler],
pttp,prov/pttp,pttp,Provisional,-,[Tony_Deng][Tuan_Hoang][Bob_Hinkle][Mark_Chen],
qb,prov/qb,qb,Provisional,-,[Jan_Pokorny],
query,prov/query,query,Provisional,-,[Dave_Thaler],
quic-transport,prov/quic-transport,quic-transport,Provisional,-,[draft-vvv-webtransport-quic],
redis,prov/redis,redis,Provisional,-,[Chris_Rebert],
rediss,prov/rediss,rediss,Provisional,-,[Chris_Rebert],
reload,,reload,Permanent,-,[RFC6940],
res,prov/res,res,Provisional,-,[Alexey_Melnikov],
resource,prov/resource,resource,Provisional,-,[Dave_Thaler],
rmi,prov/rmi,rmi,Provisional,-,[Dave_Thaler],
rsync,,rsync,Provisional,-,[RFC5781],
rtmfp,prov/rtmfp,rtmfp,Provisional,-,[RFC7425],
rtmp,prov/rtmp,rtmp,Provisional,-,[Dave_Thaler],
rtsp,,Real-Time Streaming Protocol (RTSP),Permanent,-,[RFC2326][RFC7826],
rtsps,,Real-Time Streaming Protocol (RTSP) over TLS,Permanent,-,[RFC2326][RFC7826],
rtspu,,Real-Time Streaming Protocol (RTSP) over unreliable datagram transport,Permanent,-,[RFC2326],
sarif,prov/sarif,sarif,Provisional,-,[OASIS_Open][Michael_C_Fanning][David_Keaton],
secondlife,prov/secondlife,query,Provisional,-,[Dave_Thaler],
secret-token,prov/secret-token,secret-token,Provisional,-,[RFC8959],
service,,service location,Permanent,-,[RFC2609],
session,,session,Permanent,-,[RFC6787],
sftp,prov/sftp,query,Provisional,-,[Dave_Thaler],
sgn,prov/sgn,sgn,Provisional,-,[Dave_Thaler],
shc,prov/shc,shc,Provisional,-,[Josh_Mandel],
shttp (OBSOLETE),,Secure Hypertext Transfer Protocol,Permanent,-,[RFC2660][status-change-http-experiments-to-historic],
sieve,,ManageSieve Protocol,Permanent,-,[RFC5804],
simpleledger,prov/simpleledger,simpleledger,Provisional,-,[James_Cramer],
simplex,prov/simplex,simplex,Provisional,-,[Evgeny_Poberezkin],
sip,,session initiation protocol,Permanent,-,[RFC3261],
sips,,secure session initiation protocol,Permanent,-,[RFC3261],
skype,prov/skype,skype,Provisional,-,[Alexey_Melnikov],
smb,prov/smb,smb,Provisional,-,[Dave_Thaler],
smp,prov/smp,smp,Provisional,-,[Evgeny_Poberezkin],
sms,,Short Message Service,Permanent,-,[RFC5724],
smtp,prov/smtp,smtp,Provisional,-,[draft-melnikov-smime-msa-to-mda],
snews,,NNTP over SSL/TLS,Historical,-,[RFC5538],
snmp,,Simple Network Management Protocol,Permanent,-,[RFC4088],
soap.beep,,soap.beep,Permanent,-,[RFC4227],
soap.beeps,,soap.beeps,Permanent,-,[RFC4227],
soldat,prov/soldat,soldat,Provisional,-,[Dave_Thaler],
spiffe,prov/spiffe,spiffe,Provisional,-,[Evan_Gilman],
spotify,prov/spotify,spotify,Provisional,-,[Dave_Thaler],
ssb,prov/ssb,ssb,Provisional,-,[Frédéric_Wang][Secure_Scuttlebutt_Consortium],
ssh,prov/ssh,ssh,Provisional,-,[Dave_Thaler],
starknet,prov/starknet,starknet,Provisional,-,[Abraham_Makovetsky],
steam,prov/steam,steam,Provisional,-,[Dave_Thaler],
stun,,stun,Permanent,-,[RFC7064],
stuns,,stuns,Permanent,-,[RFC7064],
submit,prov/submit,submit,Provisional,-,[draft-melnikov-smime-msa-to-mda],
svn,prov/svn,svn,Provisional,-,[Dave_Thaler],
swh,prov/swh,swh,Provisional,-,[Software_Heritage][Stefano_Zacchiroli],
swid,prov/swid,swid (see [reviewer notes]),Provisional,-,"[RFC9393, Section 5.1]",
swidpath,prov/swidpath,swidpath (see [reviewer notes]),Provisional,-,"[RFC9393, Section 5.2]",
tag,,tag,Permanent,-,[RFC4151],
taler,prov/taler,taler,Provisional,-,[draft-grothoff-taler-01],
teamspeak,prov/teamspeak,teamspeak,Provisional,-,[Dave_Thaler],
tel,,telephone,Permanent,-,[RFC3966][RFC5341],
teliaeid,prov/teliaeid,teliaeid,Provisional,-,[Peter_Lewandowski],
telnet,,Reference to interactive sessions,Permanent,-,[RFC4248],
tftp,,Trivial File Transfer Protocol,Permanent,-,[RFC3617],
things,prov/things,things,Provisional,-,[Dave_Thaler],
thismessage,perm/thismessage,multipart/related relative reference resolution,Permanent,-,[RFC2557],
tip,,Transaction Internet Protocol,Permanent,-,[RFC2371],
tn3270,,Interactive 3270 emulation sessions,Permanent,-,[RFC6270],
tool,prov/tool,tool,Provisional,-,[Matthias_Merkel],
turn,,turn,Permanent,-,[RFC7065],
turns,,turns,Permanent,-,[RFC7065],
tv,,TV Broadcasts,Permanent,-,[RFC2838],
udp,prov/udp,udp,Provisional,-,[Dave_Thaler],
unreal,prov/unreal,unreal,Provisional,-,[Dave_Thaler],
upt,historic/upt,upt,Historical,-,[IESG],
urn,,Uniform Resource Names,Permanent,-,[RFC8141][IANA registry urn-namespaces],
ut2004,prov/ut2004,ut2004,Provisional,-,[Dave_Thaler],
uuid-in-package,prov/uuid-in-package,uuid-in-package,Provisional,-,[Kunihiko_Sakamoto],
v-event,prov/v-event,v-event,Provisional,-,[draft-menderico-v-event-uri],
vemmi,,versatile multimedia interface,Permanent,-,[RFC2122],
ventrilo,prov/ventrilo,ventrilo,Provisional,-,[Dave_Thaler],
ves,prov/ves,ves,Provisional,-,[Jim_Zubov],
videotex,historic/videotex,videotex,Historical,-,[draft-mavrakis-videotex-url-spec][RFC2122][RFC3986],
vnc,,Remote Framebuffer Protocol,Permanent,-,[RFC7869],
view-source,prov/view-source,view-source,Provisional,-,[Mykyta_Yevstifeyev],
vscode,prov/vscode,vscode,Provisional,-,[urischemeowners_at_microsoft.com],
vscode-insiders,prov/vscode-insiders,vscode-insiders,Provisional,-,[urischemeowners_at_microsoft.com],
vsls,prov/vsls,vsls,Provisional,-,[urischemeowners_at_microsoft.com],
w3,prov/w3,w3 (see [reviewer notes]),Provisional,-,[Qi_Zhou],
wais,,Wide Area Information Servers,Historical,-,[RFC4156],
web3,prov/web3,web3,Provisional,-,[Qi_Zhou],
wcr,prov/wcr,wcr,Provisional,-,[Jason_Dzubak],
webcal,prov/webcal,webcal,Provisional,-,[Dave_Thaler],
web+ap,prov/web+ap,web+ap,Provisional,-,[Soni_L.],
wifi,prov/wifi,wifi,Provisional,-,[Wi-Fi_Alliance][Jun_Tian],
wpid,prov/wpid,wpid,Historical,-,[Eld_Zierau],
ws,,WebSocket connections,Permanent,[RFC8307],[RFC6455],
wss,,Encrypted WebSocket connections,Permanent,[RFC8307],[RFC6455],
wtai,prov/wtai,wtai,Provisional,-,[Dave_Thaler],
wyciwyg,prov/wyciwyg,wyciwyg,Provisional,-,[Dave_Thaler],
xcon,,xcon,Permanent,-,[RFC6501],
xcon-userid,,xcon-userid,Permanent,-,[RFC6501],
xfire,prov/xfire,xfire,Provisional,-,[Dave_Thaler],
xmlrpc.beep,,xmlrpc.beep,Permanent,-,[RFC3529],
xmlrpc.beeps,,xmlrpc.beeps,Permanent,-,[RFC3529],
xmpp,,Extensible Messaging and Presence Protocol,Permanent,-,[RFC5122],
xri,prov/xri,xri,Provisional,-,[Dave_Thaler],
ymsgr,prov/ymsgr,ymsgr,Provisional,-,[Dave_Thaler],
z39.50,,Z39.50 information access,Historical,-,[RFC1738][RFC2056],
z39.50r,,Z39.50 Retrieval,Permanent,-,[RFC2056],
z39.50s,,Z39.50 Session,Permanent,-,[RFC2056],
'''[1:-1]

def PrintStatus(fp, status="Permanent"):
    reader, out = csv.reader(fp), []
    for row in reader:
        if row[3] == status:
            out.append(row[0])
    print(f"{'-'*40}\n{status} status")
    for i in Columnize(out, indent="  "):
        print(i)
    fp.seek(0)

print("List of URI Schemes as of 30 Nov 2023")
print("  Source = https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml")
fp = StringIO(data)
PrintStatus(fp, status="Provisional")
PrintStatus(fp, status="Historical")
PrintStatus(fp, status="Permanent")
