from IPython.display import display, HTML

class NotebookGMaps(object):
    class GMapsPoint(object):
        def __init__(self, idx, lat, lng, message=None):
            self.idx = idx
            self.lat = lat
            self.lng = lng
            self.message = message

        def get_partial_js(self):
            return '''
                var infowindow{idx} = new google.maps.InfoWindow({{
                    content: '{mgs}'
                }});

                var marker{idx} = new google.maps.Marker({{
                    position: {{lat: {lat}, lng: {lng}}},
                    map: map,
                    title: {idx}
                }});

                marker{idx}.addListener('click', function() {{
                    infowindow{idx}.open(map, marker{idx});
                }});
            '''.format(
                    idx=self.idx, lat=self.lat, lng=self.lng, mgs=self.message
                )

    def __init__(self, key):
        self.key = key
        self.points = []

    def add_point(self, lat, lng, message=None):
        self.points.append(
            self.GMapsPoint(len(self.points), lat, lng, message)
        )

    def get_map_center(self, point):
        return '''{{lat: {lat}, lng: {lng}}}'''.format(
            lat=point.lat, lng=point.lng
        )

    def _create_initmap_func(self):
        return '''
            function initMap() {{
                var center = {center};
                var map = new google.maps.Map(document.getElementById('map'), {{
                    zoom: 10,
                    center: center
                }});
        '''.format(center=self.get_map_center(self.points[0])) + ''.join(
            [x.get_partial_js() for x in self.points]
        ) + '''
            }
        '''

    def _create_html_string(self):
        return '''
            <!DOCTYPE html>
            <html>
              <head>
                <style>
                  html, body { height: 100%; margin: 0; padding: 0; }
                  #map { height: 100%; }
                </style>
              </head>
              <body>
                <div id="map"></div>
                <script>
        ''' + self._create_initmap_func() + '''
                </script>
                <script src="https://maps.googleapis.com/maps/api/js?key={}&signed_in=true&callback=initMap"></script>
              </body>
            </html>
        '''.format(self.key)

    def _create_iframe(self):
        with open('tmp.html', 'w') as fout:
            fout.write(self._create_html_string())

            return '''
                <iframe src="{}" width="100%" height="300px"></iframe>
            '''.format(fout.name)

    def draw(self):
        return display(HTML(self._create_iframe()))
