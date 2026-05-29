from functools import partial
import grpc

from settings import GRPC_KEY_NAME  # Lowercase key, ASCII value



class APIKeyInterceptor(grpc.aio.ServerInterceptor):
    def __init__(self, api_key):
        # During implementation, we create the _valid_metadata attribute, which will store the secret key for validating.
        self._api_key = api_key

    async def intercept_service(self, continuation, handler_call_details):
        # Extract metadata (a list of tuples)
        metadata = dict(handler_call_details.invocation_metadata)
        
        # Check for the key (gRPC metadata keys are typically lowercase)
        print("Check if ", metadata.get(GRPC_KEY_NAME), " equals ", self._api_key)
        if metadata.get(GRPC_KEY_NAME) != self._api_key:
            # Abort the call if the key is missing or invalid
            return await self._abort_with_unauthenticated('Invalid or missing API Key')
            
        return await continuation(handler_call_details)
    
    @staticmethod
    async def deny(_, context, details):
        # A function designed to send messages to the user when errors are handled in the intercept_service function
        await context.abort(grpc.StatusCode.UNAUTHENTICATED, details)

    async def _abort_with_unauthenticated(self, details):
        async def abort(request, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, details)
        return grpc.unary_unary_rpc_method_handler(partial(self.deny, details="Key Not Found"))
