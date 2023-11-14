



[

    ["variable_setzen","cond",0],
    ["variable_setzen","showcase",["liste_erstellen",3]],
    ["liste_setzen","showcase",0,["multiplizieren",1,2,3,4]],
    ["liste_setzen","showcase",1,["dividieren",4,2]],
    ["liste_setzen","showcase",2,["hoch",3,2]],


    ["while",["ungleich",["variable_holen","cond"],3],["seq",["print",["liste_finden","showcase",["variable_holen","cond"]]],["variable_setzen","cond",["addieren",["variable_holen","cond"],1]]]],

    ["variable_setzen","first_dict",["dictionary_erstellen"]],
    ["variable_setzen","second_dict",["dictionary_erstellen"]],
    ["dictionary_setzen","first_dict",1,1],
    ["dictionary_setzen","first_dict",2,2],
    ["dictionary_setzen","first_dict",3,3],
    ["dictionary_setzen","second_dict",1,2],
    ["dictionary_setzen","second_dict",4,["dictionary_finden","first_dict",2]],
    ["variable_setzen","fused_dict",["dictionary_verbinden","first_dict","second_dict"]],
    ["print",["variable_holen","fused_dict"]]

]