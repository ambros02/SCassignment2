


[

    ["variable_setzen","init_shape",["funktion_erstellen",["name"],["seq",
        ["variable_setzen","temp",["dictionary_erstellen"]],
        ["dictionary_setzen","temp","name",["variable_holen","name"]],
        ["retournieren",["variable_holen","temp"]]
    ]]],

    ["variable_setzen","init_square",["funktion_erstellen",["name","side"],["seq",
        ["variable_setzen","temp",["dictionary_erstellen"]],
        ["dictionary_setzen","temp","name",["variable_holen","name"]],
        ["dictionary_setzen","temp","side",["variable_holen","side"]],
        ["retournieren",["variable_holen","temp"]]
    ]]],

    ["variable_setzen","init_circle",["funktion_erstellen",["name","radius"],["seq",
        ["variable_setzen","temp",["dictionary_erstellen"]],
        ["dictionary_setzen","temp","name",["variable_holen","name"]],
        ["dictionary_setzen","temp","radius",["variable_holen","radius"]],
        ["retournieren",["variable_holen","temp"]]
    ]]],


    ["variable_setzen","square_area",["funktion_erstellen",["instance"],["seq",
        ["retournieren",["hoch",["dictionary_finden",["variable_holen","instance"],"side"],2]]
        ]]],

    ["variable_setzen","circle_area",["funktion_erstellen",["instance"],["seq",
        ["retournieren",["multiplizieren",["hoch",["dictionary_finden",["variable_holen","instance"],"radius"],2],["pi"]]]
        ]]],

    ["variable_setzen","shape_density",["funktion_erstellen",["density","instance"],["seq",
        ["variable_setzen","gewicht",["variable_holen","density"]],
        ["variable_setzen","flaeche",["objekt_methode",["dictionary_finden",["variable_holen","instance"],"name"],"area",[["variable_holen","instance"]]]],
        ["retournieren",["dividieren",["variable_holen","gewicht"],["variable_holen","flaeche"]]]
        ]]],
    

    ["klasse_erstellen","Shape",[["neu","init_shape"],["dichte","shape_density"]]],
    ["klasse_erstellen","Square",[["neu","init_square"],["area","square_area"]],"Shape"],
    ["klasse_erstellen","Circle",[["neu","init_circle"],["area","circle_area"]],"Shape"],

    ["variable_setzen","sq",["objekt_instanzieren","Square",["sq",3]]],
    ["variable_setzen","ci",["objekt_instanzieren","Circle",["ci",2]]],

    
    ["variable_setzen","o",["addieren",["objekt_methode","sq","dichte",[5,"sq"]],["objekt_methode","ci","dichte",[5,"ci"]]]],
    ["print",["variable_holen","o"]]
    

]