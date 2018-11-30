from ..rel import Singleton, FP
import os, json


class Holiday( Singleton ):

    def __init__( self ):

        p = os.path.join( FP.RESOURCE.value, 'market', 'holiday' )
        with open( p, 'r' ) as f:
            self.pool = json.load( f )

    def isHoliday( self, yyyymmdd ):

        if len( str( yyyymmdd ) ) != 8:
            raise RuntimeError( 'invalid format.' )

        y = str( yyyymmdd[ :4 ] )
        c = self.pool[ y ]
        return str( yyyymmdd ) in c
