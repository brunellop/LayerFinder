def classFactory(iface):
    from .layer_finder import LayerFinder
    return LayerFinder(iface)
