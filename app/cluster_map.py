import arcgis
from arcgis.gis import GIS
# Create a GIS object, as an anonymous user for this example
gis = GIS()
# Create a map widget
map1 = gis.map('Paris') # Passing a place name to the constructor
                        # will initialize the extent of the map.
map1
map1.zoom
#suo fang ji bie can be changed 'map1.zoom = 10'

map2 = gis.map()
map2

#map2.center
map2.center = [37,144] # here we are setting the map's center to Melbourne

location = arcgis.geocoding.geocode('Central, Mel', max_locations=1)[0]
map2.extent = location['extent']

map3 = gis.map()
map3.basemaps
#print(map3.basemaps)

map3.basemap = 'dark-gray-vector'
map3

#print(map3.basemap)

# Log into to GIS that has basemap gallery option enabled.
gis = GIS("https://www.arcgis.com", "arcgis_python", "P@ssword123")
map5 = gis.map('Melbourne AU', zoomlevel=10)
map5.gallery_basemaps

#map5.basemap = 'os_open_carto'
#map5

# Log into to GIS as we will save the widget as a web map later
gis = GIS("https://www.arcgis.com", "arcgis_python", "P@ssword123")
usa_map = gis.map('AU', zoomlevel=4)  # you can specify the zoom level when creating a map
usa_map

flayer_search_result = gis.content.search("owner:esri","Feature Layer", outside_org=True)
flayer_search_result
#print(flayer_search_result)

world_timezones_item = flayer_search_result[5]
usa_map.add_layer(world_timezones_item)

world_countries_item = flayer_search_result[-2]
world_countries_layer = world_countries_item.layers[0]
world_countries_layer

usa_map.add_layer(world_countries_layer, options={'opacity':0.4})

usa_freeways = flayer_search_result[-3].layers[0]
usa_map.add_layer(usa_freeways, {'renderer':'ClassedSizeRenderer',
                                'field_name':'DIST_MILES'})

world_terrain_item = gis.content.get('58a541efc59545e6b7137f961d7de883')
terrain_imagery_layer = world_terrain_item.layers[0]
type(terrain_imagery_layer)

usa_map.add_layer(terrain_imagery_layer)

usa_map.layers

usa_map.remove_layers(layers=[usa_freeways])

usa_map.draw('rectangle')

usa_map.draw('uparrow')

from arcgis.geocoding import geocode
usa_extent = geocode('USA')[0]['extent']
usa_extent

usa_capitols_fset = geocode('Capitol', search_extent=usa_extent, max_locations=10, as_featureset=True)
usa_capitols_fset

capitol_symbol = {"angle":0,"xoffset":0,"yoffset":0,"type":"esriPMS",
                  "url":"http://static.arcgis.com/images/Symbols/PeoplePlaces/esriBusinessMarker_57.png",
                  "contentType":"image/png","width":24,"height":24}

usa_map.draw(usa_capitols_fset, symbol=capitol_symbol)

webmap_properties = {'title':'USA time zones and capitols',
                    'snippet': 'Jupyter notebook widget saved as a web map',
                    'tags':['automation', 'python']}

webmap_item = usa_map.save(webmap_properties, thumbnail='./webmap_thumbnail.png', folder='webmaps')
webmap_item

