import requests


API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYyNTU4NTY5NywiYWFpIjoxMSwidWlkIjoxMDAyODQwNTAsImlhZCI6IjIwMjYtMDItMjVUMDU6NTc6MTguMjc2WiIsInBlciI6Im1lOndyaXRlIiwiYWN0aWQiOjMzOTYwMjIzLCJyZ24iOiJhcHNlMiJ9.sFxUu3glb5tLn_Hgmb_fVxWmJq-IgOKEZEQPmfeq1Ds"

URL = "https://api.monday.com/v2"

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

def fetch_board_data(board_id):
    query = f"""
    query {{
        boards(ids: {board_id}) {{
            items_page(limit: 500) {{
                items {{
                    name
                    column_values {{
                        column {{
                            title
                        }}
                        text
                    }}
                }}
            }}
        }}
    }}
    """

    response = requests.post(URL, json={"query": query}, headers=headers)
    return response.json()