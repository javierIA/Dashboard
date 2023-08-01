window.myNamespace = Object.assign({}, window.myNamespace, {
    mySubNamespace: {
        pointToLayer: function (feature, latlng, context) {
            const { min, max, circleOptions, colorProp } = context.props.hideout;

            function lerp(start, end, amt) {
                return (1 - amt) * start + amt * end;
            }

            if (feature.properties['Tipo'] === 'Investigador') {
                let colorValue = feature.properties[colorProp];
                if (colorValue === -1 || colorValue === null) {
                    circleOptions.fillColor = 'gray';
                } else {
                    let amt = (colorValue - min) / (max - min);
                    let red = Math.floor(lerp(255, 0, amt));
                    let green = Math.floor(lerp(0, 255, amt));
                    circleOptions.fillColor = 'rgb(' + red + ',' + green + ',0)';
                }
            } else {
                circleOptions.fillColor = 'gray';
            }
            return L.circleMarker(latlng, circleOptions);
        }
    }
});
