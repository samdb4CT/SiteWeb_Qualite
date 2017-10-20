var map;
var apikey = "261bbc94c8266573016ba9454127b905b931b0a6";
var user = 'samuel';
var sublayers = [];

function init(urlMap) {
        // var urlStaticMap = "http://192.168.1.105/static/projets/RCITY/usages_par_maille.qgs";
        var urlStaticMapUsages = "\\\\NAS-FORCITY-01\\4-Equipe_technique\\2_Echanges\\SDB\\projets\\RCITY\\usages_par_maille.qgs";
        var urlStaticMapEmplois = "\\\\NAS-FORCITY-01\\4-Equipe_technique\\2_Echanges\\SDB\\projets\\RCITY\\emplois_totaux_par_maille.qgs";
        var urlStaticMapEmploisDept = "\\\\NAS-FORCITY-01\\4-Equipe_technique\\2_Echanges\\SDB\\projets\\RCITY\\rep_emplois_dynex_par_dept.qgs";
        // Base Layers : 
        var baseLayers = new ol.layer.Group(
            {   title: 'fond de plan',
            openInLayerSwitcher: true,
            layers:
                [ new ol.layer.Tile(
                    {	title: "Watercolor",
                        baseLayer: true,
                        source: new ol.source.Stamen({
                            layer: 'watercolor',
                          }),
                        visible: false
                    }),
                new ol.layer.Tile(
                    {	title: "Toner",
                        baseLayer: true,
                        visible: true,
                        source: new ol.source.Stamen({
                        layer: 'toner'
                      })
                    }),
                new ol.layer.Tile(
                    {	title: "OSM",
                        baseLayer: true,
                        source: new ol.source.OSM(),
                        visible: false
                    })
                ]
        });

        var src_usages = new ol.source.TileWMS({
                url:'/cgi-bin/qgis_mapserv.fcgi.exe?MAP='+urlStaticMapEmplois+'&',
                params:{
                    crs: 'EPSG:4326',
                    width: '800',
                    styles: '',
                    height: '550',
                    layers: 'Densité d\'emplois totaux par km² (Quantiles)',
                    format: 'image/png',
                    TILED: true,
                    bbox: '42.455888,-5.668945,50.903033,8.525391'
                    },
                serverType:'qgis'
            })
        var src_departement = new ol.source.TileWMS({
                url:'/cgi-bin/qgis_mapserv.fcgi.exe?MAP='+urlStaticMapEmplois+'&',
                params:{
                    crs: 'EPSG:4326',
                    width: '800',
                    styles: '',
                    height: '550',
                    layers: 'employment_french_department',
                    format: 'image/png',
                    TILED: true,
                    bbox: '42.455888,-5.668945,50.903033,8.525391'
                    },
                serverType:'qgis'
            })
        var src_dynex_departement = new ol.source.TileWMS({
                url:'/cgi-bin/qgis_mapserv.fcgi.exe?MAP='+urlStaticMapEmploisDept+'&',
                params:{
                    crs: 'EPSG:4326',
                    width: '800',
                    styles: '',
                    height: '550',
                    layers: 'Répartition de l\'effectif d\'emplois par secteur d\'activité Dynex',
                    format: 'image/png',
                    TILED: true,
                    bbox: '42.455888,-5.668945,50.903033,8.525391'
                    },
                serverType:'qgis'
            })
        // Couches Raster : 
        var ccIDFemployement = new ol.layer.Tile({
            title: "Densité d'emplois totaux par km²",
            id: 1,
            openInLayerSwitcher: true,
            showLegend: true,
            source:src_usages
          })
        var ccIDFdept = new ol.layer.Tile({
            title: "Départements",
            id: 2,
            openInLayerSwitcher: true,
            showLegend: true,
            source:src_departement
          })
        var ccIDFDynexdept = new ol.layer.Tile({
            title: "Répartition de l'effectif d'emplois par secteur d'activité Dynex",
            id: 2,
            openInLayerSwitcher: true,
            showLegend: true,
            source:src_dynex_departement
          })
        
        var view = new ol.View({
          center: ol.proj.fromLonLat([2.277, 48.859]),
          zoom: 8
        })
        
        // Définition des groupes de couches
        var layers1 = new ol.layer.Group(
            {   title: 'Données du City Context',
            openInLayerSwitcher: true,
            layers:
                [
                ccIDFemployement,
                ccIDFDynexdept
                ]
        });
        
        var map = new ol.Map({
        layers: [
          baseLayers,
          layers1
        ],
        target: 'map',
        view: view
        });
        // Add a layer switcher outside the map
        var switcher = new ol.control.LayerSwitcher(
            {	target:$(".layerSwitcher").get(0), 
                show_progress:true,
                extent: true,
                trash: true,
                oninfo: function (l) { alert(l.get("title")); }
            });
        map.addControl(switcher);

        // Gestion de la recherche d'information : 
        map.on('singleclick', function(evt) {
            var coordinate = evt.coordinate;
            var viewResolution = /** @type {number} */ (view.getResolution());
            var viewProjection = view.getProjection();

            var url = src_usages.getGetFeatureInfoUrl(
                evt.coordinate, 
                viewResolution, 
                viewProjection,
                'EPSG:4326',
                {'INFO_FORMAT': 'text/html'});
            if (url) {
              document.getElementById('info').innerHTML =
                  '<iframe seamless src="' + url + '"></iframe>';
            }
            });
    setPrimaryLegend(map);
}

function setPrimaryLegend(map) {
    var wmsVersion = '1.3.0';
    var format = 'image/png';
    var layers = map.getLayers().getArray();
    for (var i = 0; i < layers.length; i++) {
        if (layers[i] instanceof ol.layer.Group){
            var layersFromGroup = layers[i].getLayers().getArray();
            for (var j=0; j < layersFromGroup.length; j++){
                if (layersFromGroup[j].get('showLegend') === true && layersFromGroup[j].getProperties().visible) {
                    try {
                        var url = layersFromGroup[j].getSource().getUrls()[0];
                    } catch (err) {
                        var url = layersFromGroup[j].getSource().getUrl();
                    }
                    var legendImg = $('#sidebar').append('<img id=img_'+layersFromGroup[j].get('id')+' src="'+url + 'REQUEST=GetLegendGraphic&SERVICE=WMS&layer=' + layersFromGroup[j].getSource().getParams().layers + '&format=' + format + '"></img>');
                }
            }
        }
        else{
            if (layers[i].get('showLegend') === true && layersFromGroup[j].getProperties().visible) {
                try {
                    var url = layers[i].getSource().getUrls()[0];
                } catch (err) {
                    var url = layers[i].getSource().getUrl();
                }
                var legendImg = $('#sidebar').append('<img id=img_'+layers[i].get('id')+' src="'+url + 'REQUEST=GetLegendGraphic&SERVICE=WMS&layer=' + layersFromGroup[j].getSource().getParams().layers + '&format=' + format + '"></img>');
            }
        }
    }
}

function getJSON(req){
    $.ajaxSetup( { "async": false } );
    return $.getJSON(req);
}