#Add hyperlinks to each reference to one of the 29 CA Codes
# Todo: This does not always work over a newline (\n)
{
/Code of/ {N; s/Code\sof\sCivil\sProcedure/<a href="\/laws\/target\/Code-ccp">Code of Civil Procedure<\/a>/sg;}
s/Business\sand\sProfessions\sCode/<a href="\/laws\/target\/Code-bpc">Business and Professions Code<\/a>/Sg;
s/Civil\sCode/<a href="\/laws\/target\/Code-civ">Civil Code<\/a>/Sg;
s/Commercial\sCode/<a href="\/laws\/target\/Code-com">Commercial Code<\/a>/Sg;
s/Corporations\sCode/<a href="\/laws\/target\/Code-corp">Corporations Code<\/a>/Sg;
s/Education\sCode/<a href="\/laws\/target\/Code-edc">Education Code<\/a>/Sg;
s/Elections\sCode/<a href="\/laws\/target\/Code-elec">Elections Code<\/a>/Sg;
s/Evidence\sCode/<a href="\/laws\/target\/Code-evid">Evidence Code<\/a>/Sg;
s/Family\sCode/<a href="\/laws\/target\/Code-fam">Family Code<\/a>/Sg;
s/Financial\sCode/<a href="\/laws\/target\/Code-fin">Financial Code<\/a>/Sg;
s/Fish\sand\sGame\sCode/<a href="\/laws\/target\/Code-fgc">Fish and Game Code<\/a>/Sg;
s/Food\sand\sAgricultural\sCode/<a href="\/laws\/target\/Code-fac">Food and Agricultural Code<\/a>/Sg;
s/Government\sCode/<a href="\/laws\/target\/Code-gov">Government Code<\/a>/Sg;
s/Harbors\sand\sNavigation\sCode/<a href="\/laws\/target\/Code-hnc">Harbors and Navigation Code<\/a>/Sg;
s/Health\sand\sSafety\sCode/<a href="\/laws\/target\/Code-hsc">Health and Safety Code<\/a>/Sg;
s/Insurance\sCode/<a href="\/laws\/target\/Code-ins">Insurance Code<\/a>/Sg;
s/Labor\sCode/<a href="\/laws\/target\/Code-lab">Labor Code<\/a>/Sg;
s/Military\sand\sVeterans\sCode/<a href="\/laws\/target\/Code-mvc">Military and Veterans Code<\/a>/Sg;
s/Penal\sCode/<a href="\/laws\/target\/Code-pen">Penal Code<\/a>/Sg;
s/Probate\sCode/<a href="\/laws\/target\/Code-prob">Probate Code<\/a>/Sg;
s/Public\sContract\sCode/<a href="\/laws\/target\/Code-pcc">Public Contract Code<\/a>/Sg;
s/Public\sResources\sCode/<a href="\/laws\/target\/Code-prc">Public Resources Code<\/a>/Sg;
s/Public\sUtilities\sCode/<a href="\/laws\/target\/Code-puc">Public Utilities Code<\/a>/Sg;
s/Revenue\sand\sTaxation\sCode/<a href="\/laws\/target\/Code-rtc">Revenue and Taxation Code<\/a>/Sg;
s/Streets\sand\sHighways\sCode/<a href="\/laws\/target\/Code-shc">Streets and Highways Code<\/a>/Sg;
s/Unemployment\sInsurance\sCode/<a href="\/laws\/target\/Code-uic">Unemployment Insurance Code<\/a>/Sg;
s/Vehicle\sCode/<a href="\/laws\/target\/Code-veh">Vehicle Code<\/a>/Sg;
s/Water\sCode/<a href="\/laws\/target\/Code-wat">Water Code<\/a>/Sg;
s/Welfare\sand\sInstitutions\sCode/<a href="\/laws\/target\/Code-wic">Welfare and Institutions Code<\/a>/Sg;
}

#/Section/ s_(Section\s)([0-9.]*)(\)?\s)(.*?)(of\s?the\s.*Code(\d{1,2}))_\1<a href="/laws/target/Code\6-\2">\2</a>\3\4\5_Sg;

