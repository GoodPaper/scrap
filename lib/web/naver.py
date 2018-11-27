from .misc import get
import re


class Naver( object ):

    PatternDateTime = r'\b\d{4}.\d{2}.\d{2}\b'

    def __init__( self ):

        self.uroot = 'https://finance.naver.com/'
        self.uinst = self.uroot + 'item/main.nhn?code={code}'

        self.uquot = self.uroot + 'sise/sise_index.nhn?code={mkt}'
        self.adkey = ( 'upper', 'rise', 'steady', 'fall', 'lower' )

        # self.ureco = https://recommend.finance.naver.com/Home/RecommendSummary/naver
        self.ucons = 'https://companyinfo.stock.naver.com/company/c1010001.aspx?cmp_cd={code}'

    def verify( self, cond ):

        if not cond:
            raise RuntimeError( 'please check html.' )

    def quoteAD( self, market ):

        soup = get(
            url = self.uquot.format( mkt = market ),
            soup = True
        )
        rest = soup.find_all( 'table', { 'class': 'table_kos_index' } )
        self.verify( len( rest ) == 1 )

        ads = rest[ 0 ].find_all( 'li' )
        self.verify( len( ads ) == 5 )

        extr = dict.fromkeys( self.adkey )
        for k in self.adkey:
            for i in ads:
                a = i.find_all( 'a' )
                self.verify( len( a ) == 1 )
                href = a[ 0 ].attrs[ 'href' ]
                self.verify( href is not None or href != '' )
                if k in href:
                    extr[ k ] = int( a[ 0 ].find_all( 'span' )[ 0 ].text )

        return extr

    def instConsensus( self, code ):

        soup = get(
            url = self.ucons.format( code = code ),
            soup = True
        )

        ds = None
        rest = soup.find_all( 'div', { 'class': 'all-width' } )
        for c in rest:
            dt = c.find_all( 'dd', { 'class': 'header-table-cell unit' } )
            if all( x is not None for x in dt ) and len( dt ) == 1:
                ds = re.findall( Naver.PatternDateTime, dt[ 0 ].text )[ 0 ]
                break
        self.verify( ds is not None )

        rest = soup.find_all( 'table', { 'class': 'gHead all-width', 'id': 'cTB15' } )
        self.verify( len( rest ) == 1 )
        rest = rest[ 0 ].find_all( 'td' )
        self.verify( len( rest ) == 6 )
        cons = dict()
        for idx, r in enumerate( rest ):
            if 'noline-bottom' in r.attrs[ 'class' ]:
                if idx == 1:    cons[ 'opinion' ] = r.text.strip()
                elif idx == 2:  cons[ 'target' ] = r.text.strip()
                elif idx == 3:  cons[ 'eps' ] = r.text.strip()
                elif idx == 4:  cons[ 'per' ] = r.text.strip()
                elif idx == 5:  cons[ 'recogov' ] = r.text.strip()
        self.verify( len( cons ) > 0 )

        rest = soup.find_all( 'table', { 'class': 'gHead01 all-width', 'id': 'cTB24' } )
        self.verify( len( rest ) == 1 )
        rest = rest[ 0 ].find_all( 'tbody' )
        self.verify( len( rest ) == 1 )
        rest = rest[ 0 ].find_all( 'tr' )
        reco = list()
        for r in rest:
            tds = r.find_all( 'td' )
            z = dict()
            for idx, c in enumerate( tds ):
                if idx == 0:    z[ 'agency' ] = c.text.strip()
                elif idx == 1:  z[ 'date' ] = c.text.strip()
                elif idx == 2:  z[ 'targetPrice' ] = c.text.strip()
                elif idx == 3:  z[ 'prevTarget' ] = c.text.strip()
                elif idx == 4:  z[ 'changeRatio' ] = c.text.strip()
                elif idx == 5:  z[ 'opinion' ] = c.text.strip()
                elif idx == 6:  z[ 'prevOpinion' ] = c.text.strip()
            reco.append( z )

        return ds, cons, reco

