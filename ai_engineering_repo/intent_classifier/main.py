from router.router import route_query

if __name__ == "__main__":

    while True:

        query = input("\nQuestion: ")

        if query.lower() == "exit":
            break

        result = route_query(query)

        print(result)