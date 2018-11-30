import enum, os


class FP( enum.Enum ):

    ROOT = os.path.abspath(
        os.path.join(
            os.path.dirname(
                os.path.realpath( __file__ )
            ),
            '..', '..'
        )
    )

    APP = os.path.join( ROOT, 'app' )
    LIB = os.path.join( ROOT, 'lib' )
    DATA = os.path.join( ROOT, 'data' )
    RESOURCE = os.path.join( ROOT, 'resource' )
