if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Search for chemical names, old and new
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    import re
if 1:   # Custom imports
    from wrap import dedent
    from color import PrintMatch
if 1:   # Global variables
    chemical_data = dedent('''
    Acetic ether	Ethyl acetate	C2H5O2C2H3
    Acetone                     	Dimethyl ketone, 2-propanone	OC(CH3)2
    Acid of air	Carbon dioxide	CO2
    Acid of ants	Formic acid	
    Acid of apples	Malic acid	
    Acid of lemon	Citric acid	
    Acid of milk	Lactic acid	
    Acid of salt	Hydrochloric acid	HCl
    Acid of sugar               	Oxalic acid                   	H2C2O4·H20
    Acid potassium sulphate     	Potassium bisulphate          	KHSO4
    Acidum saltus	Hydrochloric acid	HCl
    Ackey                       	Nitric acid                   	HNO3
    Aer urinosa	Ammonia	
    Alcali volatil              	Ammonium hydroxide            	NH4OH
    Alcohol sulphuris	Carbon disulfide	CS2
    Alcohol, grain              	Ethyl alcohol (ethanol)       	C2H5OH
    Alcohol, wood               	Methyl alcohol (methanol)     	CH3OH
    Alembroth, salt of 		Hg2(NH4)2Cl4·H2O 
    Algaroth, powder of 		SbOCl
    Alizarin	1,2-dihydroxyanthraquinone, a red dye	C14H8O4
    Alizarin black	Naphtharazine, 5,8-dihydroxy-1,4-naphthoquinone, a black dye 	C10H6O4
    Alizarin blue	A dihydroxyanthraquinone quinoline 	C17H9O4
    Alizarin bordeaux	1,2,3-trihydroxyanthraquinone, a dye derived from anthraquinone 	C14H8O5
    Alizarin brown	1,2,3-trihydroxyanthraquinone, a dye derived from anthraquinone 	C14H8O5
    Alizarin red	Alizarin sodium sulfonate, the sodium salt of the sulfonic acid of alizarin; an acid-base indicator	NaC14H7O7S
    Alizarin yellow	Sodium p-nitraniline salicylate, an acid-base indicator	C13H10NO5
    Alum                        	Aluminum potassium sulfate    	AlK(SO4)2·12H2O
    Alumina                     	Aluminum oxide                	Al2O3
    Alundum                     	Fused aluminum oxide          	Al2O3
    Ammonia                     	Ammonium hydroxide            	NH4OH
    Aniline purple	Mauveine, the first aniline dye	C27H24N4
    Anthracene blue	A dihydroxyanthraquinone quinoline 	C17H9O4
    Antichlor                   	Sodium thiosulfate            	Na2S2O3·5H2O
    Antimony black              	Antimony trisulfide          	Sb2S3
    Antimony bloom	Antimony oxide	Sb2O3
    Antimony flowers                	antimony oxysulphide          	Sb2S3 + Sb2O3
    Antimony glance	Stibnite, antimony sulfide mineral	Sb2S3
    Antimony ochre	Stibiconite, an antimony mineral	Sb2O3(OH)2
    Antimony red                	antimony oxysulphide          	Sb2S3 + Sb2O3
    Antimony vermillion         	antimony oxysulphide          	Sb2S3 + Sb2O3
    Aqua ammonia                	Ammonium hydroxide solution   	NH4OH + H20
    Aqua fortis                 	Nitric acid                   	HNO3
    Aqua regia                  	Nitric & hydrochloric acid    	HNO3 + HCl
    Aqua vitae	Aqueous ethanol	C2H5OH
    Argentum	Silver	Ag
    Arnaudon's green	Chromium phosphate	CrPO4
    Aromatic spirits of ammonia 	Ammonia gas in alcohol        	...
    Arsenic glass               	Arsenic trioxide              	As4O6
    Asbestos                    	Magnesium silicate            	Mg3Si2O7·2H2O
    Ascorbic acid	Vitamin C	C6H8O6
    Aspirin                     	Acetylsalicylic acid          	C2H3O2C6H4CO2H
    Aurum	Gold	Au
    Azotic air	Nitrogen	N2
    Azurite                     	Mineral form of basic copper carbonate	CuCO3
    Baker's salt	Ammonium carbonate	(NH4)2CO3
    Baking soda                 	Sodium bicarbonate            	NaHCO3
    Banana oil                  	Amyl acetate                  	CH3CO2C5H11
    Barilla	Impure sodium carbonate	
    Barium  white               	Barium sulfate                	BaSO4
    Barium white	Barium sulfate	BaSO4
    Baryta                      	Barium oxide                  	BaO
    Bauxite                     	Impure aluminum oxide         	Al2O3
    Benzal green	Triphenylmethane dye, acid-base indicator	C23H25N2Cl
    Benzine	Ligroin or petroleum ether; sometimes benzene	
    Benzol                      	Benzene                       	C6H6
    Bicarbonate of soda         	Sodium hydrogen carbonate or sodium bicarbonate	NaHCO3
    Bichloride of mercury       	Mercuric chloride             	HgCl2
    Bichrome                    	Potassium dichromate          	K2Cr2O7 
    Bismuth ochre	Bismite	Bi2O3·3H2O 
    Bitter salt	Magnesium sulfate (Epsom salts)	MgSO4·7H2O
    Bitter salt                 	Magnesium sulphate            	MgSO·7H2O
    Black ash	Impure sodium carbonate mixed with unburnt carbon	
    Black ash                   	Crude form of sodium carbonate	Na2CO3
    Black lead                  	Graphite                      	C
    Black oxide of copper       	Cupric oxide                  	CuO
    Black oxide of mercury      	Mercurous oxide               	Hg2O
    Black precipitate	A black powder	Hg2O·Hg2NH2NO3
    Black silver	Stephanite, a silver antimony sulfide mineral	5Ag2S·Sb2S 
    Blanc-fixe                  	Barium sulfate                	BaSO4
    Bleaching powder	Formed by passing chlorine gas over dry calcium hydroxide; with water, it is a mixture of CaCl2 and Ca(OCl)2.	
    Bleaching powder            	Calcium hypochlorite          	CaOCl2
    Blue copperas               	Copper sulfate                	CuSO4·5H2O
    Blue lead                   	Lead sulfate                  	PbSO4
    Blue salts                  	Nickel sulfate                	NiSO4·7H2O
    Blue stone                  	Copper sulfate                	CuSO4·5H2O
    Blue vitriol                	Copper sulfate                	CuSO4·5H2O
    Bogore	Bog iron ore	2Fe2O3·3H2O
    Bone ash                    	Impure calcium carbonate      	CaCO3 + ? 
    Bone black	Impure charcoal from bones and blood	
    Boracic acid         	Boric acid                    	H3BO3
    Borax                	Sodium borate                 	Na2B4O7·10H2O
    Bremen blue	Copper carbonate	
    Brimstone            	Sulfur                        	S
    Brine                	Strong NaCl solution          	NaCl + H2O
    Brown ochre	Bog iron ore	2Fe2O3·3H2O
    Brunswick green	Copper oxychloride or copper carbonate	CuOCl·Cu(OH)2
    Burnt alum           	Anhydrous potassium aluminum sulfate	...
    Burnt lime           	Calcium oxide                 	CaO
    Burnt ochre          	Ferric oxide                  	Fe2O3
    Burnt ore            	Ferric oxide                  	Fe2O3
    Butter of antimony   	Antimony trichloride          	SbCl3
    Butter of tin        	Anhydrous stannous chloride   	SnCl4 + 5H2O
    Butter of X	Chloride or trichloride of X	...
    Butter of zinc       	Zinc chloride + 1/4 its weight in water   	ZnCl2 + H2O
    Calcareous earth	Calcium oxide	CaO
    Caliche              	Impure sodium nitrate         	NaNO3
    Calomel              	Mercurous chloride            	Hg2Cl2
    Carbolic acid        	Phenol                        	C6H5OH
    Carbonate of lime	Calcium carbonate	CaCO3
    Carbonic acid	Carbon dioxide	CO2
    Carbonic acid gas    	Carbon dioxide                	CO2
    Carburetted hydrogen	Methane	CH4
    Caro's acid	Permonosulfuric acid 	H2SO5
    Cassel yellow	Lead oxychloride	PbCl2·2PbO
    Caustic earth	Calcium hydroxide	Ca(OH)2
    Caustic lime         	Calcium hydroxide             	Ca(OH)2
    Caustic potash       	Potassium hydroxide           	KOH
    Caustic soda         	Potassium hydroxide           	KOH
    Caustic vegetable alkali	Potassium hydroxide	KOH
    Ceruse	Lead carbonate	2PbCO3·Pb(OH)2
    Chalk                	Calcium carbonate             	CaCO3
    Chamber crystals	Nitrosyl sulfate	NO·HSO4
    Chile nitre          	Sodium nitrate                	NaNO3
    Chile saltpeter      	Sodium nitrate                	NaNO3
    Chinese red          	Basic lead chromate           	PbCrO4
    Chinese white        	Zinc oxide                    	ZnO
    Chloride of lime     	Calcium hypochlorite          	Ca(ClO)2
    Chloride of soda     	Sodium hypochlorite           	NaOCl
    Chlorinated lime	Bleaching powder	
    Chloroform           	Trichloromethane              	CHCl3
    Chrome alum          	Chromium potassium sulfate    	CrK(SO4)3·12H2O
    Chrome green         	Chromium oxide                	Cr2O3
    Chrome red	Lead chromate	PbCrO4·PbO
    Chrome yellow	Lead chromate	PbCrO4
    Chromic acid         	Chromium trioxide             	CrO3
    Cinnabar	Mercury sulfide, a red pigment	HgS
    Cobalt blue	A pigment containing cobalt oxide, CoO, zinc oxide, Zn, and chalcedony, an amorphous quartz, SiO2	
    Cobalt green	A green pigment, solid solution of cobalt and zinc oxides, CoO and ZnO	
    Cobalt red	Erythrite, a native cobalt arsenate	Co3(AsO4)2· 8H2O 
    Cobalt violet	Cobalt phosphate, a pigment in oil paints	Co3(PO4)2 ·2H2O 
    Cobalt yellow	Cobalt potassium nitrite	K3Co(NO2)6·xH2O
    Colcothar	Iron oxide (Paris red)	Fe2O3
    Columbium	Niobium	Nb
    Concrete volatile alkali	Ammonium carbonate	(NH4)2CO3
    Congo blue	Blue dye	C17H12N3O7S2Na2
    Congo red	Red dye	C32H22N6O6S2Na2
    Congo yellow	Orange-red dye	C24H18O4N5SNa 
    Copperas             	Ferrous sulfate               	FeSO4·7H2O
    Corrosive sublimate  	Mercuric chloride             	HgCl2
    Corundum             	Aluminum oxide                	Al2O3
    Coupier's blue	Blue dye	C24H18N2
    Cream of tartar	Potassium bitartrate purified into small white crystals	KHC4H4O6
    Creech	Calcium sulfate	CaSO4
    Cremor tartari	Tartar purified into small white crystals	KHC4H4O6
    Cresol purple	m-cresolsulfonphthalein, acid-base indicator	C21H18O5S
    Cresol red	o-cresolsulfonphthalein, acid-base indicator	C21H18O5S
    Crocus	A yellow or reddish powdered calx (oxide)	
    Crocus of antimony	Impure antimony oxysulfide	
    Crocus of copper	Cuprous oxide	Cu2O
    Crocus of iron	Iron sesquioxide or peroxide	
    Crocus of lead	Red lead	
    Crocus powder        	Ferric oxide                  	Fe2O3
    Crystal carbonate    	Sodium carbonate              	Na2CO3
    Cyanocobalamin	Vitamin B12	C63H90CoN14O14P
    DDT                  	Dichlorodiphenyltrichloroethane	(C6H)*Cl2*CH*CCl3
    Dechlor             	Sodium thiophosphate        	Na3(PO3)3S XH2O, x=12-18
    Diamine blue	Blue dye	C17H12N3O7S2Na2
    Diamond             	Carbon crystal              	C
    Diuretic salt	Potassium acetate	KC2H3O
    Dry ice             	Solid carbon dioxide        	CO2
    Dutch liquid        	Ethylene dichloride         	CH2Cl*CH2Cl
    Dutch oil	Ethylene chloride	C2H4Cl2
    Dydymium	Mixture of Pr and Nd	
    Earth	A metal oxide	
    Emery powder        	Impure aluminum oxide       	Al2O3
    Epsom salts         	Magnesium sulfate           	MgSO4·7H2O
    Ethanol             	Ethyl alcohol               	C2H5OH
    Ether               	Ethyl ether                 	(C2H5)2O
    Ethiops mineral 	Mercury sulfide	Hg2S
    Ethyl gas	Leaded gasoline (i.e., includes tetraethyllead (C2H5)4Pb as an additive)	
    Everitt's salt	Potassium ferrous ferrocyanide	K2Fe[Fe(CN)6]
    Farina              	Starch                      	Complex carbohydrate
    Ferro prussiate     	Potassium ferricyanide      	K3Fe(CN)6
    Ferrum              	Iron                        	Fe
    Fixed vegetable alkali	Crude or purified potassium carbonate	K2CO3
    Fixed white         	Barium sulfate              	BaSO4
    Flores Martes       	Anhydrous ferric chloride   	Fe2Cl6
    Flores martiales	Ferriammonium chloride	NH4FeCl4
    Flowers of sulphur  	Sulfur                      	S
    Flowers of X	Oxide of X (X is usually a metal)	...
    Fluor, fluorspar	Calcium fluoride	CaF2
    Fluorspar           	Natural calcium fluoride    	CaF2
    Folic acid	Vitamin Bc	C19H19N7O6
    Formalin            	Formaldehyde                	HCOH
    Fossil alkali	Sodium carbonate	
    French chalk        	Natural magnesium silicate  	H2Mg3(SiO3)4
    French vergidris    	Basic copper acetate        	Cu(C2H2O2)2·H20
    Fulminating silver	Silver nitride	Ag3N
    Galena              	Natural lead sulfide        	PbS
    Glacial	Glass-like, crystalized	
    Glance	Mineral with a glassy appearance	
    Glauber's salt      	Sodium sulfate              	Na2SO4·10H2O
    Glucinium or glucinum	Beryllium	Be
    Grain alcohol       	Ethyl alcohol               	C2H5OH
    Green lion	Iron sulfate	FeSO4
    Green salt	Uranium fluoride	UF4
    Green verditer      	Basic copper carbonate      	CuCO3
    Green vitriol       	Ferrous sulfate             	FeSO4·7H2O
    Gun cotton          	Cellulose nitrate           	C6H8(NO2)2O5
    Gypsum              	Natural calcium sulfate     	CaSO4·5H2O
    Hahnemann's mercury	A black powder	Hg2O·Hg2NH2NO3
    Hard oil            	Boiled linseed oil          	...
    Heavy spar          	Barium sulfate              	BaSO4
    Hepar	Sulfide	
    Hepatic air	Hydrogen sulfide	H2S
    Hepatic air	Hydrogen sulfide	H2S
    Homberg's salt	Boric acid	B(OH)3
    Horn silver	Native silver chloride	AgCl
    Hydrargyrum	Mercury	Hg
    Hydrated lime	Calcium hydroxide	Ca(OH)2
    Hydrocyanic acid    	Hydrogen cyanide            	HCN
    Hypo                	Sodium thiosulfate          	Na2S2O3·5H2O
    Indian red          	Ferric oxide                	Fe2O3
    Iron perchloride    	Ferric chloride             	FeCl3·6H2O
    Iron pernitrate     	Ferric nitrate              	Fe(NO3)3·9H2O
    Iron persulphate    	Ferric sulfate              	Fe(SO4)3·nH2O
    Iron protochloride  	Ferrous chloride            	FeCl2·4H2O
    Isinglass           	Agar-agar gelatin	...
    Javelle water       	Originally potassium hypochlorite solution, now usually sodium hypochlorite 	Originally KOCl + H2O, now NaOCl + H2O
    Jeweler's etchant   	3 g silver nitrate + 3 g nitric acid + 3 g mercurous nitrate + 100 cc H2O	HgNO3·H2O + AgNO3 + HNO3 + H2O
    Jeweler's rouge          	Ferric oxide                  	Fe2O3
    K.N.S. solution          	10 g ammonium carbonate + 20 g ammonium peroxydisulphide + 200 cc ammonium hydroxide  	NH4CO3·H2O + (NH4)2S2O8 + NH4OH
    Kalium	Potassium	K
    Killed spirits           	Zinc chloride                 	ZnCl2
    King's yellow	Arsenic sulfide	As2S3
    Kurrol's salt	Potassium phosphate	(KPO3)4
    Labarraque's solution    	Sodium hypochlorite solution  	NaOCl + H2O
    Lampblack                	Crude form of carbon, charcoal	C
    Lapis causticus	Fused sodium or potassium hydroxide	
    Lapis imperialis	Silver nitrate	AgNO3
    Lapis lunarius	Fused silver nitrate	AgNO3
    Laughing gas             	Nitrous oxide                 	N2O
    Lead black	Graphite	C
    Lead peroxide            	Lead dioxide                  	PbO2
    Lead protoxide           	Lead oxide                    	PbO
    Lead white	Lead carbonate	2PbCO3·Pb(OH)2
    Lead, red	Lead oxide	Pb3O4
    Leipzig yellow	Lead chromate	PbCrO4
    Libavius, fuming liquor of	Tin tetrachloride	SnCl4
    Lime                     	Calcium oxide                 	CaO
    Lime, slaked             	Calcium hydroxide             	Ca(OH)2
    Lime, unslaked           	Calcium oxide                 	CaO
    Limewater                	Calcium hydroxide solution    	Ca(OH)2 + H2O
    Liquor ammonia           	Ammonium hydroxide solution   	NH4OH
    Litharge                 	Lead oxide                    	PbO
    Lithopone                	Zinc sulfide + barium sulfate 	ZnS + BaSO4
    Liver of sulphur         	Melted potassium carbonate + sulphur	K2CO3 + S
    Lunar caustic            	Silver nitrate                	AgNO3
    Lye	Potassium hydroxide solution	KOH
    Magnesia                 	Magnesium oxide               	MgO
    Magnesia alba levis	Magnesium carbonate and magnesium oxide	4MgCO3·Mg(OH)2 ·5H2O
    Magnesia nigra	Pyrolusite, natural manganese dioxide	MnO2
    Magnesite                	Magnesium carbonate           	MgCO3
    Magnus salt	Tetrammineplatinum tetrachloroplatinate	Pt(NH3)4PtCl4
    Malachite green	Copper carbonate	Cu2(OH)2CO3
    Manganese black          	Manganese dioxide             	MnO2
    Manganese green	Barium manganate	BaMnO4
    Manganese red	Rhodonite MnSiO3 or rhodochrosite MnCO3	
    Marble                   	Calcium carbonate             	CaCO3
    Marignac salt	Potassium tin sulfate	K2Sn(SO4)2
    Marine acid 	Hydrochloric acid 	HCl
    Marine alkali	Sodium carbonate	
    Marsh gas                	Methane                       	CH4
    Martius yellow	The calcium salt of naphthalene yellow	
    Massicot	Lead oxide (yellow)	PbO
    Mercurial nitre	Mercuric nitrate	Hg(NO3)2
    Mercurius calcinatus per se	Mercuric oxide	HgO
    Mercury oxide, black     	Mercury(II) oxide             	HgO
    Metanil yellow	Sodium salt of 4'-aniline azobenzenesulfonic acid, an acid-base indicator	C12H10N3O3SNa
    Methanol                 	Methyl alcohol                	CH3OH
    Methyl green	A triphyenylmethane dye and acid-base indicator	C25H30N3Cl
    Methyl orange	Sodium p-dimethylaminobenzenesulfonate, an acid-base indicator	C14H14O3N3SNa
    Methyl red	o-dimethylaminoazobenzenecarboxylic acid, an acid-base indicator	C15H15O2N3
    Methylated spirits       	Methyl alcohol                	CH3OH
    Methylene blue	3,9-bisdimethylaminophenazothionium chloride trihydrate, an acid-base indicator	C16H18N3SCl·3H2O
    Microcosmic salt	Sodium ammonium phosphate 	NaNH4HPO4·4H2O
    Mild earth	Calcium carbonate	CaCO3
    Mild vegetable alkali	Crude or purified potassium carbonate	K2CO3
    Milk of barium	Barium hydroxide + water	Ba(OH)2
    Milk of bismuth	Bismuth nitrates + water	Bi(OH)2NO3 and/or BiOH(NO3)2
    Milk of lime             	Calcium hydroxide + water       	Ca(OH)2
    Milk of magnesia         	Magnesium hydroxide + water   	Mg(OH)2
    Milk of sulfur           	Precipitated sulfur           	S
    Millon's base	Formed from a solution of mercuric oxide in ammonium chloride	(HOHg)2NH2OH
    Mineral alkali, common	Hydrated sodium carbonate	
    Mineral dye blue	A blue copper or tungsten ore, or a mixture of ferriferrocyanide, Fe4[Fe(CN)6]3, with calcium or barium sulfate 	
    Mineral dye green	Copper carbonate	
    Mineral dye purple	Reddish iron oxide pigment	
    Mineral dye white	Hydrated calcium sulfate	
    Mineral dye yellow	Lead oxychloride	PbCl2·2PbO
    Minium	Red lead oxide	Pb3O4
    Mohr salt	Ferrous ammonium sulfate	(NH4)2Fe(SO4)2 ·6H2O
    Molybdic ochre	Molybdite, yellow molybdenum oxide	MoO3
    Monsel salt	Iron sub-sulfate 	Fe4(SO4)5O
    Monthier blue	Blue pigment	FeNH4[Fe(CN)6]
    Mosaic gold	Tin sulfide pigment	SnS2
    Muriate of lime	Calcium chloride	CaCl2
    Muriate of mercury       	Mercuric chloride             	HgCl2
    Muriate of X     	Chloride of X	...
    Muriatic acid            	Hydrochloric acid             	HCl
    Muriatic ether	Ethyl chloride	C2H5Cl
    Mustard gas	A di(chloroethyl)sulfide	(ClCH2CH2)2S
    Naphthalene yellow	A dinitro 1-naphthol	C10H5(NO2)2OH
    Naples yellow	Lead antimoniate, a yellow pigment	Pb3(SbO4)2
    Natron                   	Sodium carbonate              	Na2CO3
    Natural gas              	Mostly methane                	CH4
    Neutral red	Dimethyldiaminotoluphenazine hydrochloride, an acid-base indicator	
    Niacin	Vitamin B3	C6H5NO2
    Niagra blue	Blue dye	C17H12N3O7S2Na2
    Nickel bloom	Annabergite, a green mineral	Ni3As2O2·8H2O
    Nickel ochre	Annabergite, a green mineral	Ni3As2O2·8H2O
    Nicotinic acid	Vitamin B3	C6H5NO2
    Nile blue	Aniline dye and acid-base indicator	C20H19ON3
    Niter                    	Potassium nitrate             	KNO3
    Niton	Radon	Rn
    Nitrate of silver        	Silver nitrate                	AgNO3
    Nitre                    	Potassium nitrate             	KNO3
    Nitre or niter	Potassium nitrate	KNO3
    Nitric ether	Ethyl nitrate	C2H5NO3
    Nitrous air	Nitric dioxide (laughing gas)	N2O
    Nitrous ether	Ethyl nitrite	C2H5NO2
    Nitrous ether	Ethyl nitrite	C2H5NO2
    Nordhausen acid	Fuming sulfuric acid; i.e. a solution of sulfur trioxide, SO3, in concentrated (about 98%) sulfuric acid	H2SO4 + SO3
    Norwegian nitre	Calcium nitrate	Ca(NO3)2
    Oil of ants	Furfural	C5H4O2
    Oil of apples	Amyl valerate (n-pentyl pentanoate)	C4H9COC5H11
    Oil of bananas	n-pentyl acetate 	CH3COC5H11
    Oil of bitter almonds    	Benzaldehyde                  	C6H5CHO
    Oil of cognac	Ethyl hexyl ether (enanthic ether)	C6H13OC2H5
    Oil of garlic	Allyl sulfide	(C3H5)2S
    Oil of glonoin	Nitroglycerin	C3H5N3O9
    Oil of mars              	Deliquescent anhydrous ferric chloride     	FeCl3 + H2O
    Oil of mirbane           	Nitrobenzene                  	C6H5NO2
    Oil of mustard, artificial	Allyl isothiocyanate	C3H5NCS
    Oil of pears	n-pentyl acetate 	CH3COC5H11
    Oil of pineapple	Ethyl butyrate	C3H7COOC2H5
    Oil of tartar	A saturated solution of potassium carbonate	K2CO3
    Oil of vitriol           	Sulfuric acid                 	H2SO4
    Oil of wintergreen       	Methyl salicylate             	C6H4OHCOOCH3
    Olefiant gas	Ethene	C2H4
    Oleum	Fuming sulfuric acid; i.e. a solution of sulfur trioxide, SO3, in concentrated (about 98%) sulfuric acid	H2SO4 + SO3
    Orpiment                 	Arsenic trisulfide            	As2S3
    Orthophosphoric acid     	Phosphoric acid               	H3PO4
    Oxygenated muriatic acid	Chlorine	Cl2
    Oxymuriate of mercury     	Mercuric chloride            	HgCl2
    Oxymuriate of potassium   	Potassium chlorate           	KClO3
    Oxymuriatic acid	Chlorine	Cl2
    Paris blue                	Ferric ferrocyanide,         	Fe7(CN)18(H2O)x where 14 <= x <= 16
    Paris green               	Copper aceto-arsenite	3Cu(AsO2)2·Cu(C2H3O2)2
    Paris red	Red lead oxide	Pb3O4
    Paris white               	Powdered calcium carbonate   	CaCO3
    Paris yellow	Lead chromate	PbCrO4
    Patent yellow	Lead oxychloride	PbO·PbCl2
    Pear essence              	Isoamyl acetate, also called banana oil	C7H14O2
    Pearl ash	Impure calcined potassium carbonate	K2CO3
    Péligot's salt	Potassium chlorochromate 	KCrO3Cl
    Perkin's mauve	Mauveine, the first aniline dye	C27H24N4
    Perkin's violet	Mauveine, the first aniline dye	C27H24N4
    Permanent white           	Barium sulfate               	BaSO4
    Peroxide                  	Hydrogen peroxide solution   	H2O2 + H2O
    Phenol red	Phenolsulfonphthalein, an acid-base indicator	C19H14O5S
    Phosgene                  	Carbonyl chloride            	COCl2
    Phosphine		PH3
    Phosphuretted hydrogen	Phosphine	PH3
    Plaster of Paris          	Calcium sulfate              	(CaSO4)2·H2O
    Plessy's green	Chromium phosphate	CrPO4
    Plimmer's salt	Sodium antimony tartrate	Na(SbO)C4H4O6
    Plumbago	A lead ore, including lead oxide (litharge) or lead sulfide (galena); or graphite	
    Plumbic ochre	Brown lead oxide	PbO2
    Plumbum	Lead	Pb
    Plumbum album	Lead carbonate	2PbCO3·Pb(OH)2
    Plumbum candidum	Lead carbonate	2PbCO3·Pb(OH)2
    Pompholix	Crude zinc oxide	ZnO
    Potash                    	Potassium carbonate          	K2CO3
    Potassa                   	Potassium hydroxide          	KOH
    Precipitated chalk        	Calcium carbonate            	CaCO3
    Prussian blue	Complex salts used in inks and dyes resulting from the oxidation of the white precipitate of a solution of iron(II) sulfate, FeSO4, and potassium ferrocyanide, K4Fe(CN)6	Fe7(CN)18(H2O)x where 14 <= x <= 16
    Prussic acid              	Hydrocyanic acid             	HCN
    Purple crystals           	Potassium permanganate       	KMnO4
    Pyridoxin	Vitamin B6	C8H11NO3
    Pyrite	Originally any "fire-stone" from which sparks could be struck; eventually an iron sulfide or iron-copper sulfide	
    Pyro                      	Pyrogallic acid              	C6H3(OH)3
    Pyroacetic spirit	Acetone	(CH3)2CO
    Pyroligneous acid	Distillate from wood, containing acetic acid, methanol, and acetone	
    Pyroligneous spirit	Methanol	CH3OH
    Pyroxylic spirit	Methanol	CH3OH
    Quicklime	Calcium oxide	CaO
    Quicksilver               	Mercury                      	Hg
    Racemic acid	An optically inactive form of tartaric acid consisting of equal quantities of optical isomers	
    Radium A	218Po, ? = 3 minutes	
    Radium C	214Bi, ? = 20 minutes; 214Po (C'); C2 210Tl, ? = 1.3 minutes	
    Radium D	210Pb, ? = 21 years	
    Radium E	210Bi	
    Radium F	210Po, ? = 140 days	
    Radium G	206Pb	
    Realgar	Arsenic sulfide	As2S2
    Red arsenic	Arsenic sulfide	As2S2
    Red lead	Red lead oxide	Pb3O4
    Red liquor                	Aluminum acetate solution    	(CH3CO2)2AlOH
    Red ochre	Hematite	Fe2O3
    Red orpiment	Arsenic sulfide	As2S2
    Red oxide of copper       	Cuprous oxide                	Cu2O
    Red oxide of mercury      	Mercuric oxide               	HgO
    Red prussiate	Potassium ferricyanide 	K3Fe(CN)6
    Red prussiate of potash   	Potassium ferricyanide       	KC3Fe(CN)6
    Red prussiate of soda     	Sodium ferrocyanide          	Na4Fe(CN)6
    Red vitriol	Cobalt sulfate	CoSO4·7H2O
    Regulus	Antimony	Sb
    Reinecke's acid	Tetrathiocyanodiammonochromic acid 	HCr(NH3)2(SCN)4
    Reinecke's salt	An ammonium salt of Reinecke's acid 	NH4[Cr(NH3)2(SCN)4]·H2O
    Retinol	A fat-soluble vitamin derived from carotenes 	C20H30O
    Riboflavin	Vitamin B2	C17H20N4O6
    Rochelle salt             	Potassium sodium tartrate    	KNaC4H4O6·4H2O
    Rock salt                 	Sodium chloride              	NaCl
    Roman vitriol                	Copper sulfate                	CuSO4·5H2O
    Rose vitriol	Cobalt sulfate	CoSO4·7H2O
    Rouge                     	Ferric oxide                 	Fe2O3
    Rouge, jeweler's          	Ferric oxide                 	Fe2O3
    Rough nitre	Magnesium chloride	MgCl2
    Rubbing alcohol           	Isopropyl alcohol            	CH3CHOHCH3
    Ruby	Red corundum	Al2O3
    Ruby arsenic	Arsenic sulfide	As2S2
    Ruby blende	Red sphalerite (zinc sulfide)	ZnS
    Ruby copper	Cuprite, copper oxide	Cu2O
    Ruby silver	Proustite	Ag3AsS3
    Ruby sulfur	Arsenic sulfide	As2S2
    Saccharum saturni	Sugar of lead; lead acetate	
    Sal acetosella	Potassium hydrogen oxalate 	KHC2O4
    Sal aeratus	Potassium hydrogen carbonate 	KHCO3
    Sal albus	Borax	
    Sal alembroth	Insoluble white powder	HgNH2Cl
    Sal ammoniac              	Ammonium chloride            	NH4Cl
    Sal armoniack	Ammonium chloride	NH4Cl
    Sal commune	Sodium chloride	NaCl
    Sal de duobus	Potassium sulfate 	K2SO4
    Sal enixum	Glauber's salt	
    Sal fossile	Sodium chloride	NaCl
    Sal marinum	Sodium chloride	NaCl
    Sal nitri	Nitre	
    Sal nitrum	Nitre	
    Sal sapientiae	Mercury ammonium chloride 	HgNH2Cl
    Sal soda                  	Crystalline sodium carbonate 	NaHCO3
    Sal spaientiae	Insoluble white powder	HgNH2Cl
    Sal volatile              	Ammonium carbonate           	(NH4)2CO3
    Saleratus	Potassium hydrogen carbonate or sodium bicarbonate	KHCO3 or NaHCO3
    Salt                      	Sodium chloride              	NaCl
    Salt cake                 	Impure sodium sulfate        	Na2SO4
    Salt of hartshorn	Ammonium carbonate	(NH4)2CO3
    Salt of lemon	Potassium hydrogen oxalate 	KHC2O4
    Salt of tartar	Solid potassium carbonate 	K2CO3
    Salt of vitriol	Zinc sulfate	ZnSO4·7H2O
    Salt of wormwood          	Potassium carbonate          	K2CO3
    Saltpeter                 	Potassium nitrate            	KNO3
    Saltpeter (Chile)         	Impure sodium nitrate        	NaNO3
    Salts of hartshorn        	Ammonium carbonate           	(NH4)2CO3
    Salts of lemon            	Potassium binoxalate         	KHC2O4·H2O
    Salts of sorrol           	Potassium acid oxalate       	KHC2O4·H2O
    Salts of tartar           	Potassium carbonate          	K2CO3
    Scheele's green	Acidic copper arsenite	CuHAsO3
    Schlippe's salt	Sodium sulfantimonate 	Na3SbS4·9H2O
    Schllkopf's acid	One of 1-naphthol-4,8-disulfonic acid, 1-naphthylamine-4,8-disulfonic acid, and 1-naphthylamine-8-sulfonic acid	
    Seignette's salt	Rochelle salt	
    Silica                    	Silicon dioxide              	SiO2
    Siliceous earth	Silicon dioxide	SiO2
    Silver glance	Argentite, silver sulfide	Ag2S
    Slaked lime               	Calcium hydroxide            	Ca(OH)2
    Soapstone                 	Impure magnesium silicate    	H2Mg3(SiO3)4
    Soda	Sodium carbonate	Na2CO3
    Soda ash                  	Dry sodium carbonate         	Na2CO3
    Soluble glass	Hydrated sodium silicate	Na2Si4O9·xH2O
    Sorrel salt	Potassium hydrogen oxalate 	KHC2O4
    Spanish green	Copper acetate (verdigris)	Cu(C2H2O2)2·H20
    Spanish white	Bismuth oxychloride, BiOCl, or oxynitrate, BiONO3	
    Spencer's acid              	3 g silver nitrate + 3 g nitric acid + 3 g mercurous nitrate + 100 cc	HgNO3·H2O + AgNO3 + HNO3 + H2O
    Spirit of alum	Sulfuric acid	H2SO4
    Spirit of colonial	Methanol	CH3OH
    Spirit of Columbian	Methanol	CH3OH
    Spirit of hartshorn         	Ammonia gas in alcohol (Given in Gunsmith Kinks II as ammonium hydroxide)	...
    Spirit of nitre	Nitric acid or ethyl nitrite	HNO3 or C2H5NO2
    Spirit of nitrous ether     	Ethyl nitrate                 	C2H5NO2
    Spirit of salt	Hydrochloric acid	HCl
    Spirit of vitriol	Sulfuric acid	H2SO4
    Spirit of wine	Concentrated aqueous ethanol	C2H5OH + H2O
    Spirit of wood	Methanol	CH3OH
    Spirits of salt             	Hydrochloric acid             	HCl
    Spirits of wine             	Ethyl alcohol                 	C2H5OH
    Spiritus saltus	Hydrochloric acid	HCl
    Spiritus vini	Concentrated aqueous ethanol	C2H5OH + H2O
    Stannum glaciale	Bismuth (literally glacial tin)	Bi
    Sugar of lead               	Lead acetate                  	Pb(C2H3O2)2·3H20
    Sulfur per campanum	Sulfuric acid	H2SO4
    Sulfuric ether	Diethyl ether	
    Sulfuric ether              	Ethyl ether                   	(C2H5)2O
    Sulphovinic acid	Ethyl hydrogen sulfate	C2H5·HSO4
    Sulphuret	Sulfide	
    Sulphuretted	Combined or impregnated with sulfur	
    Sulphuretted hydrogen	Hydrogen sulfide	H2S
    Sulphurous acid	Sulfur dioxide	SO2
    Sulphurous gas	Sulfur dioxide	SO2
    Sweet salt	Sodium chlorite	NaClO2
    Sweet spirit of nitre	Ethyl nitrite	C2H5NO2
    Sweet spirits of nitre      	Ethyl nitrite solution with ethyl alcohol 	C2H5NO2 + C2H5OH
    Sylvius's febrifuge salt	Potassium chloride	KCl
    Talc                        	Magnesium silicate            	H2Mg3(SiO3)4
    Tartar	Potassium hydrogen tartrate 	KHC4H4O6
    Tartar emetic	Potassium antimonyl tartrate	KSbOC4H4O6·1/2H2O
    Tartar of wine	Potassium hydrogen tartrate 	KHC4H4O6
    Tectum argenti	Bismuth	Bi
    Telluric ochre	Yellow tellurium oxide	TeO2
    Terra ponderosa	Barium oxide	BaO
    Terra ponderosa aerata	Barium carbonate	BaCO3
    Tetrachloromethane          	Carbon tetrachloride          	CCl4
    Thénard's blue	Blue cobalt aluminate 	Co(AlO2)2
    Thiamin	Also thiamine, vitamin B1	C12H17N4OSCl 
    Thorium A	216Po, ? = 150 ms	
    Thorium C	212Bi, ? = 61 minutes; C' is 212Po, ? = 300 ns.	
    Thorium D	208Tl, ? = 3 minutes	
    Thorium X	224Ra, ? = 3.6 days	
    Thymol blue	Thymolsulphonphthalein, an acid-base indicator	C27H30O5S
    Tin salt                    	Stannous chloride             	SnCl2
    Tincture of ferric chloride 	Ferric chloride + ethyl alcohol	FeCl3·6H2O + C2H5OH
    Tincture of steel           	Ferric chloride + ethyl alcohol	FeCl3·6H2O + C2H5OH
    TNT                         	Trinitrotoluene               	C6H2CH3(NO3)3
    Toluol                      	Toluene                       	C6H5CH3
    Toluylene red	Dimethyldiaminotoluphenazine hydrochloride, an acid-base indicator	
    Trona	Natural sodium carbonate/bicarbonate	Na2CO3·NaHCO3·2H2O
    Trypan blue	Blue dye	C17H12N3O7S2Na2
    Tungstic ochre	Yellow tungsten oxide	WO3
    Turbith mineral	Basic sulfate of mercury	HgSO4·2HgO
    Turnbull's blue	Ferroferricyanide 	Fe3[Fe(CN)6]2
    Turpeth	Basic sulfate of mercury	HgSO4·2HgO
    Tyrian purple	6,6'-dibromoindigotin, a dye of the ancient Mediterranean	C16H8N2O2Br2
    Uranic ochre	Uraconite, a yellow uranium oxide	U2O3
    Uranium I	238U	
    Uranium II	234U, ? = 2.5?105 years	
    Uranium X	X1 = 234Th, = 24 days, X2 = 234Pa	
    Uranium yellow	Sodium uranate, a pigment used in glass and ceramics 	Na2UO4
    Uranivitriol	A uranium sulfate	
    Urinous air	Ammonia	
    Urinous salt	An ammonium salt; occasionally any alkaline salt.	
    Vegetable alkali	Crude or purified potassium carbonate	K2CO3
    Verdigris                   	Copper acetate                	Cu(C2H2O2)2·H20
    Vermillion	Mercury sulfide, a red pigment	HgS
    Victoria green	Triphenylmethane dye, acid-base indicator	C23H25N2Cl
    Vinegar                     	Dilute and impure acetic acid 	CH3COOH
    Vitamin A	A fat-soluble vitamin derived from carotenes 	C20H30O
    Vitamin B	A group of water-soluble, heat labile compounds that typically serve as co-enzymes. They include many examples that contain amine groups (as in "vital amine"). 	
    Vitamin B1	Thiamin	C12H17N4OSCl 
    Vitamin B12	Cyanocobalamin	C63H90CoN14O14P
    Vitamin B2	Riboflavin	C17H20N4O6
    Vitamin B3	Niacin	C6H5NO2
    Vitamin B6	Pyridoxin	C8H11NO3
    Vitamin Bc	Folic acid	C19H19N7O6
    Vitamin C	Ascorbic acid	C6H8O6
    Vitamin D	This fat-soluble vitamin consists of steroid derivatives including ergocalciferol, C28H44O, and cholecalciferol, C27H44O	
    Vitamin E	This vitamin occurs in four naturally occuring forms, called ?-, ?-, ?-, and ?-tocopherol. The ? form, C29H50O2, has the greatest activity; the ?- and ?- forms have one fewer methyl group, and the ?- form two fewer.	
    Vitriol	A sulfate	
    Vitriol                     	Sulfuric acid                 	H2SO4
    Vitriolate of tartar	Potassium sulfate	K2SO4
    Vitriolic acid	Sulfuric acid	H2SO4
    Volatile alkali	Aqueous ammonia, NH3	
    Washing soda                	Crystalline sodium carbonate  	Na2CO3
    Water glass	Hydrated sodium silicate	Na2Si4O9·xH2O
    White arsenic               	Arsenic trioxide              	As2O3
    White lead                  	Basic lead carbonate          	(PbCO3)2·Pb(OH)2
    White precipitate	Insoluble white powder	HgNH2Cl
    White vitriol               	Zinc sulfate                  	ZnSO4·7H2O
    Whitewash                   	Solution of quick lime or slaked lime used as a cheap substitute for paint.	...
    Whiting                     	Powdered calcium carbonate    	CaCO3
    Wolfram	Tungsten	W
    Wood alcohol                	Methyl alcohol                	CH3OH
    Xylenol blue	1,4-dimethyl-5-hydroxybenzenesulfonphthalein, an acid-base indicator	
    Xylol                       	Xylene                        	C6H4(CH3)2
    Yellow arsenic	Arsenic sulfide	As2S3
    Yellow ochre	Mixture of powdered iron oxide and clay	
    Yellow precipitate	Yellow mercury oxide	HgO
    Yellow prussiate	Potassium ferricyanide	K3Fe(CN)6·3H2O
    Yellow prussiate of potash  	Potassium ferrocyanide        	K4Fe(CN)6·3H2O
    Zinc white                  	Zinc oxide                    	ZnO
    ''')
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] regex1 ...
      Search for a chemical name in a database of old and new names.  The
      regular expressions are OR'd together.  Examples:  
        * Search for 'vitriol' to find a number of sulfates.
        * Search for 'sugar' to what 'sugar of lead' is (it was used as
          a sweetener before its toxicity was known).
    Options:
        -i      Make the search case-sensitive
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-i"] = False
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-i",):
            d[o] = not d[o]
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    if not args:
        Usage(d)
    return args
def GetData():
    '''Return the chemical data as a list of lists; each list contains
    three strings:  [old_name, modern_name, formula].
    '''
    data = []
    for i in chemical_data.split("\n"):
        s = [j.strip() for j in i.split("\t")]
        if len(s) != 3:
            print("Bad line:")
            print(s)
            exit()
        data.append(s)
    return data
def SearchLine(regexps, line, d):
    '''
    '''
    for r in regexps:
        mo = r.search(line)
        if mo:
            PrintMatch(line, r)
            return
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    data = ['; '.join(i) for i in GetData()]
    regexps = []
    case = 0 if d["-i"] else re.I
    for i in args:
        regexps.append(re.compile(i, case))
    for line in data:
        SearchLine(regexps, line, d)
