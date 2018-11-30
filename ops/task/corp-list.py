from lib.web import Kind
from lib.rel import FP
from lib.misc import Holiday
from datetime import datetime
import sys, os, tarfile, io


class Handler( object ):

    def __init__( self, repo ):

        self.date = datetime.today().strftime( '%Y%m%d' )
        self.agnt = Kind()
        if not os.path.isdir( repo ):
            raise RuntimeError( 'invalid repo path.' )
        self.repo = repo

    def __call__( self ):

        self.isHoliday()
        for m in Kind.Market.keys():
            d = self.agnt.codes( m )
            self.archive( m, d )

    def isHoliday( self ):

        if Holiday().isHoliday( self.date ):
            raise RuntimeError( '{} is holiday.'.format( self.date ) )

    def archive( self, market, content ):

        c, d = self.isChanged( market, content )
        self.stamp( market, content )
        if c:
            self.historical( content, d )

    def isChanged( self, market, today ):

        fltr =[ x for x in os.listdir( self.repo ) if market in x ]
        if len( fltr ) == 0:
            return True, []

        o = self.previous( market )
        if len( set( today ) - set( o ) ) == 0:
            return True, o
        else:
            return False, None

    def previous( self, market ):

        fltr =[ x for x in os.listdir( self.repo ) if market in x and self.date not in x ]
        p = sorted( fltr )[ 0 ]
        p = os.path.join( self.repo, p )

        with tarfile.open( p, 'r:bz2' ) as tar:
            m = tar.getnames()
            if len( m ) != 1:
                raise RuntimeError( 'invalid archive.' )
            obj = tar.extractfile( m[ 0 ] )
            ctnt = [ Kind.Corp( *( x.split( ',' ) ) ) for x in obj.readlines() ]

        return ctnt

    def stamp( self, market, content ):

        f = '{0}-{1}.csv'.format( market.lower(), self.date )
        a = '{0}-{1}.tar.bz2'.format( market.lower(), self.date )
        p = os.path.join( self.repo, a )

        if os.path.exists( a ):
            raise RuntimeError( '{} is already in.'.format( a ) )

        obj = io.BytesIO()
        obj.writelines( [ ( ','.join( x ) + '\n' ).encode() for x in content ] )

        i = tarfile.TarInfo( f )
        i.size = obj.tell()
        obj.seek( 0 )
        with tarfile.open( p, 'w:bz2' ) as tar:
            tar.addfile( i, fileobj = obj )

    def historical( self, today, diff ): pass


def main():

    path = os.path.join( FP.DATA.value, 'instruments' )
    if not os.path.exists( path ):
        os.makedirs( path )
    Handler( path )()


if __name__ == '__main__':

    sys.exit( main() )
