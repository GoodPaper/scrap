from .misc import get
from collections import namedtuple
import urllib.parse


class Kind( object ):

    Market = {
        'kospi': 'stockMkt',
        'kosdaq': 'kosdaqMkt',
        'konex': 'konexMkt'
    }
    Corp = namedtuple( 'Corp', [ 'name', 'code', 'sector', 'product', 'ipo', 'closing', 'ceo', 'homepage', 'location' ] )

    def __init__( self ):

        self.base = 'kind.krx.co.kr/corpgeneral/corpList.do'

    def codes( self, market, delisted = False ):

        parm = dict( method = 'download' )
        if market.lower() in Kind.Market.keys():
            parm[ 'marketType' ] = Kind.Market.get( market )
        if not delisted:
            parm[ 'searchType' ] = 13

        prms = urllib.parse.urlencode( parm )
        rurl = urllib.parse.urlunsplit( ( 'http', self.base, '', prms, '' ) )

        soup = get( url = rurl, soup = True )
        trs = soup.find_all( 'tr' )

        corp = list()
        for r in trs:
            tds = r.find_all( 'td' )
            if len( tds ) > 0:
                corp.append( Kind.Corp( *[ x.text.strip() for x in tds ] ) )

        return corp
