body = [
            {
                "type": "Try",
                "body": [
                    {
                        "type": "Assign",
                        "targets": [
                            {
                                "type": "Name",
                                "id": "result",
                                "ctx": {
                                    "type": "Store"
                                },
                                "lineno": 4,
                                "col_offset": 8,
                                "end_lineno": 4,
                                "end_col_offset": 14
                            }
                        ],
                        "value": {
                            "type": "BinOp",
                            "left": {
                                "type": "Name",
                                "id": "a",
                                "ctx": {
                                    "type": "Load"
                                },
                                "lineno": 4,
                                "col_offset": 17,
                                "end_lineno": 4,
                                "end_col_offset": 18
                            },
                            "op": {
                                "type": "Div"
                            },
                            "right": {
                                "type": "Name",
                                "id": "b",
                                "ctx": {
                                    "type": "Load"
                                },
                                "lineno": 4,
                                "col_offset": 21,
                                "end_lineno": 4,
                                "end_col_offset": 22
                            },
                            "lineno": 4,
                            "col_offset": 17,
                            "end_lineno": 4,
                            "end_col_offset": 22
                        },
                        "type_comment": None,
                        "lineno": 4,
                        "col_offset": 8,
                        "end_lineno": 4,
                        "end_col_offset": 22
                    },
                    {
                        "type": "Assign",
                        "targets": [
                            {
                                "type": "Name",
                                "id": "result",
                                "ctx": {
                                    "type": "Store"
                                },
                                "lineno": 5,
                                "col_offset": 8,
                                "end_lineno": 5,
                                "end_col_offset": 14
                            }
                        ],
                        "value": {
                            "type": "BinOp",
                            "left": {
                                "type": "Name",
                                "id": "a",
                                "ctx": {
                                    "type": "Load"
                                },
                                "lineno": 5,
                                "col_offset": 17,
                                "end_lineno": 5,
                                "end_col_offset": 18
                            },
                            "op": {
                                "type": "Div"
                            },
                            "right": {
                                "type": "Name",
                                "id": "b",
                                "ctx": {
                                    "type": "Load"
                                },
                                "lineno": 5,
                                "col_offset": 21,
                                "end_lineno": 5,
                                "end_col_offset": 22
                            },
                            "lineno": 5,
                            "col_offset": 17,
                            "end_lineno": 5,
                            "end_col_offset": 22
                        },
                        "type_comment": None,
                        "lineno": 5,
                        "col_offset": 8,
                        "end_lineno": 5,
                        "end_col_offset": 22
                    },
                    {
                        "type": "Assign",
                        "targets": [
                            {
                                "type": "Name",
                                "id": "result",
                                "ctx": {
                                    "type": "Store"
                                },
                                "lineno": 6,
                                "col_offset": 8,
                                "end_lineno": 6,
                                "end_col_offset": 14
                            }
                        ],
                        "value": {
                            "type": "BinOp",
                            "left": {
                                "type": "Name",
                                "id": "a",
                                "ctx": {
                                    "type": "Load"
                                },
                                "lineno": 6,
                                "col_offset": 17,
                                "end_lineno": 6,
                                "end_col_offset": 18
                            },
                            "op": {
                                "type": "Div"
                            },
                            "right": {
                                "type": "Name",
                                "id": "b",
                                "ctx": {
                                    "type": "Load"
                                },
                                "lineno": 6,
                                "col_offset": 21,
                                "end_lineno": 6,
                                "end_col_offset": 22
                            },
                            "lineno": 6,
                            "col_offset": 17,
                            "end_lineno": 6,
                            "end_col_offset": 22
                        },
                        "type_comment": None,
                        "lineno": 6,
                        "col_offset": 8,
                        "end_lineno": 6,
                        "end_col_offset": 22
                    }
                ],
                "orelse": [],
                "finalbody": [],
                "lineno": 3,
                "col_offset": 4,
                "end_lineno": 8,
                "end_col_offset": 38
            },
            {
                "type": "Return",
                "value": {
                    "type": "Name",
                    "id": "result",
                    "ctx": {
                        "type": "Load"
                    },
                    "lineno": 9,
                    "col_offset": 11,
                    "end_lineno": 9,
                    "end_col_offset": 17
                },
                "lineno": 9,
                "col_offset": 4,
                "end_lineno": 9,
                "end_col_offset": 17
            }
        ]

for i in range(len(body)):
    if "body" in body[i]:
        for j in range(len(body[i]["body"])):
            print(body[i]["body"][j]["value"]["op"]["type"])
            print(body[i]["body"][j]["value"]["lineno"])


