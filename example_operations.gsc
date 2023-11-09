


[
    ["dictionary_erstellen","namesdad"],
    ["dictionary_erstellen","dskadpk"],
    ["dictionary_erstellen","names"],
    ["dictionary_erstellen","vier"],
    ["seq",
        ["dictionary_setzen","namesdad","drei","second"],
        ["dictionary_setzen","namesdad","first","test"],
        ["dictionary_setzen","vier","first","second"],
        ["dictionary_setzen","dskadpk","second",2],
        ["dictionary_setzen","names","first","namesdad"],
        ["dictionary_setzen","names","second","dskadpk"],
        ["dictionary_verbinden",["dictionary_finden","names","first"],["dictionary_finden","names",["dictionary_finden","namesdad","drei"]],"newone"]
    ],
    ["dictionary_erstellen",["dictionary_finden","newone","first"]],
    ["dictionary_setzen","test","second",2],
    ["dictionary_setzen","newone", ["dictionary_finden","test","second"],"test_value"],
    ["dictionary_setzen","newone", "thiskey", [1,2,3,4]]
]