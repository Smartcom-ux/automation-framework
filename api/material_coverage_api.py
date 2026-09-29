class MaterialCoverageAPI:

    def __init__(self, context):
        self.context = context

    def get_open_so_details(self, api_url):

        response = self.context.request.get(
            api_url,
            params={
                "AOD": "true"
            }
        )

        return response