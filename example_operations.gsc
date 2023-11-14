

[
    ["variable_setzen","foo",["funktion_erstellen",["name"],["seq",
        ["variable_setzen","temp",["dictionary_erstellen"]],
        ["dictionary_setzen","temp","name",["variable_holen","name"]],
        ["retournieren",["variable_holen","temp"]]
    ]]],

    ["variable_setzen","faa",["funktion_erstellen",["x"],["seq",
        ["retournieren",1]
    ]]],

    ["variable_setzen","baa",["funktion_erstellen",["x"],["seq",
        ["retournieren",2]
    ]]],
    ["variable_setzen","oll",["funktion_erstellen",[],["seq",
        ["variable_setzen","y","baa"],
        ["funktion_aufrufen",["variable_holen","y"],[1]]
    ]]],

    ["variable_setzen","olll",["funktion_erstellen",[],["seq",
        ["variable_setzen","y","baa"],
        ["funktion_aufrufen",["variable_holen","y"],[1]]
    ]]],

    ["variable_setzen","haa",["funktion_erstellen",["x"],["seq",
        ["variable_setzen","baa",["funktion_erstellen",["x"],["seq",
            ["retournieren",2]
        ]]],
        ["retournieren",["funktion_aufrufen","baa",[1]]],
        ["retournieren",["funktion_aufrufen","baa",[1]]]
    ]]],



    ["klasse_erstellen","X",[["neu","foo"],["start","faa"]]],
    ["klasse_erstellen","Y",[["fart","baa"]],"X"],
    ["variable_setzen","x", ["objekt_instanzieren","X",["ho"]]],
    ["variable_setzen","y", ["objekt_instanzieren","Y",["ha"]]],
    ["variable_setzen","a",["objekt_methode","x","start",[1]]],
    ["variable_setzen","b",["objekt_methode","y","fart",[1]]],
    ["variable_setzen","laa",["funktion_aufrufen","haa",[1]]],
    ["objekt_methode","y","start",[1]],
    ["funktion_aufrufen","oll",[]],
    ["funktion_aufrufen","olll",[]],
    ["variable_setzen","po",["liste_erstellen",5]],
    ["variable_setzen","o",1],
    ["liste_setzen","po",3,"hello_world"],
    ["print",["liste_finden","po",3]],
    ["print",["hoch",2,2]],
    ["print",["multiplizieren",2,2]],
    ["print",["dividieren",2,2]],
    ["print",["addieren",2,2]],
    ["print",["pi"]],
    ["while",["ungleich",["variable_holen","o"],4],["seq",["print",["addieren",2,2]],["variable_setzen","o",["addieren",["variable_holen","o"],1]]]]
    
]