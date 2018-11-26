from .misc import get


class Naver( object ):

    def __init__( self ):

        self.uroot = 'https://finance.naver.com/'
        self.uinst = self.uroot + 'item/main.nhn?code={code}'

        self.uquot = self.uroot + 'sise/sise_index.nhn?code={mkt}'
        self.adkey = ( 'upper', 'rise', 'steady', 'fall', 'lower' )

        # self.ureco = https://recommend.finance.naver.com/Home/RecommendSummary/naver
        self.ucons = 'https://companyinfo.stock.naver.com/company/c1010001.aspx?cmp_cd={code}'

    def verify( self, cond ):

        if not cond:
            raise RuntimeError( 'plase check html.' )

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
             self.ucons.format( code = code )
         )



