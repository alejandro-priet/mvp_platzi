    <!-- ============== Js Files ==============  -->
        let longitude, latitude;
        const contentString =
        '<div class="card">' +
        '<div class="card-header">Card Header</div>' +
        '<div class="card-body">' +
        '<h5 class="card-title">Title</h5>' +
        '<p class="card-text">With supporting text below as a natural lead-in to additional content.</p>'+
        '<a href="#" class="btn btn-primary">Go somewhere</a>'+
        '</div>'+
        '<div class="card-footer">'+
        'This is card footer'+
        '</div></div>';
        <!-- ============= Geo Localization ======== -->
        function ipLookUp () {
          $.ajax('http://ip-api.com/json')
          .then(
              function success(response) {
                  console.log('User\'s Location Data is ', response);
                  console.log('User\'s Country', response.country);
                  getAddress(response.lat, response.lng)
        },

              function fail(data, status) {
                  console.log('Request failed.  Returned status of',
                              status);
              }
          );
        }

        function getAddress (latitude, longitude) {
          $.ajax('https://maps.googleapis.com/maps/api/geocode/json?' +
                  'latlng=' + latitude + ',' + longitude + '&key=' +
                  'AIzaSyCPl2iHJylG3zBfQ9TJs2voLPlBnz_IITA')
          .then(
            function success (response) {
              console.log('User\'s Address Data is ', response)
            },
            function fail (status) {
              console.log('Request failed.  Returned status of',
                          status)
            }
           )
        }

        if ("geolocation" in navigator) {
          // check if geolocation is supported/enabled on current browser
          navigator.geolocation.getCurrentPosition(
           function success(position) {
             // for when getting location is a success
             //getAddress(position.coords.latitude, position.coords.longitude)
               latitude = position.coords.latitude
               longitude = position.coords.longitude

            // This example adds a search box to a map, using the Google Place Autocomplete
            // feature. People can enter geographical searches. The search box will return a
            // pick list containing a mix of places and predicted search terms.
            // This example requires the Places library. Include the libraries=places
            // parameter when you first load the API. For example:
            // <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

              const map = new google.maps.Map(document.getElementById("map"), {
                center: { lat: latitude, lng: longitude },
                zoom: 15,
                mapTypeId: "roadmap",
                zoomControl: false,
                mapTypeControl: false,
                  scaleControl: false,
                  streetViewControl: false,
                  rotateControl: true,
                  fullscreenControl: false
              });
              // Set LatLng and title text for the markers. The first marker (Boynton Pass)
                // receives the initial focus when tab is pressed. Use arrow keys to
                // move between markers; press tab again to cycle through the map controls.
                const tourStops = [
                [{ lat: latitude, lng: longitude }, "Example position"],
                ];
                // Create an info window to share between markers.
                const infoWindow = new google.maps.InfoWindow();
                // Create the markers.
                tourStops.forEach(([position, title], i) => {
                const marker = new google.maps.Marker({
                  position,
                  map,
                  title: `${i + 1}. ${title}`,
                  label: `${i + 1}`,
                  optimized: false,
                  icon: {
                      url: "static/assets/img/icon/maps.png",
                      scaledSize: new google.maps.Size(50, 50) // pixels
                  }
                });
                // Add a click listener for each marker, and set up the info window.
                marker.addListener("click", () => {
                  infoWindow.close();
                  infoWindow.setContent(contentString); //marker.getTitle()
                  infoWindow.open(marker.getMap(), marker);
                });
                });

              // Create the search box and link it to the UI element.
              const input = document.getElementById("pac-input");
              const searchBox = new google.maps.places.SearchBox(input);
              map.controls[google.maps.ControlPosition.TOP_CENTER].push(input);
              // Bias the SearchBox results towards current map's viewport.
              map.addListener("bounds_changed", () => {
                searchBox.setBounds(map.getBounds());
              });
              let markers = [];
              // Listen for the event fired when the user selects a prediction and retrieve
              // more details for that place.
              searchBox.addListener("places_changed", () => {
                const places = searchBox.getPlaces();

                if (places.length === 0) {
                  return;
                }
                // Clear out the old markers.
                markers.forEach((marker) => {
                  marker.setMap(null);
                });
                markers = [];
                // For each place, get the icon, name and location.
                const bounds = new google.maps.LatLngBounds();
                places.forEach((place) => {
                  if (!place.geometry || !place.geometry.location) {
                    console.log("Returned place contains no geometry");
                    return;
                  }
                  const icon = {
                    url: place.icon,
                    size: new google.maps.Size(71, 71),
                    origin: new google.maps.Point(0, 0),
                    anchor: new google.maps.Point(17, 34),
                    scaledSize: new google.maps.Size(25, 25),
                  };
                  // Create a marker for each place.
                  markers.push(
                    new google.maps.Marker({
                      map,
                      icon,
                      title: place.name,
                      position: place.geometry.location,
                    })
                  );

                  if (place.geometry.viewport) {
                    // Only geocodes have viewport.
                    bounds.union(place.geometry.viewport);
                  } else {
                    bounds.extend(place.geometry.location);
                  }
                });
                map.fitBounds(bounds);
              });
           },
          function error(error_message) {
            // for when getting location results in an error
            console.error('An error has occurred while retrieving' +
                          'location', error_message)
            ipLookUp()
          });
        } else {
          // geolocation is not supported
          // get your location some other way
          console.log('geolocation is not enabled on this browser')
          ipLookUp()
        }