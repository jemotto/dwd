$(function () {
	'use strict';

    const API_SERVER='http://{{BACKEND_HOSTNAME}}:{{BACKEND_PORT}}'

    var Selection = Backbone.Model.extend({
      defaults: {
        variable: undefined,
        station: undefined
      }
    });
    var selection = new Selection();

    Vue.component('jemo-dropdown-menu', {
        data: function() {
            return {
                selectedOption: undefined,
                showMenu: false
            }
        },
        props: {
            placeholderText: String,
            options: Array,
            selectionAttr: String
        },
        methods: {
            updateOption(option) {
                this.selectedOption = option;
                this.showMenu = false;
                selection.set(this.selectionAttr, this.selectedOption);
            },

            toggleMenu() {
              this.showMenu = !this.showMenu;
            }
        },
        template: `
            <div class="btn-group">
                <li @click="toggleMenu()" class="dropdown-toggle" v-if="selectedOption !== undefined">
                  {{ selectedOption.name }}
                  <span class="caret"></span>
                </li>

                <li @click="toggleMenu()" class="dropdown-toggle" v-if="selectedOption === undefined">
                  {{ placeholderText }}
                  <span class="caret"></span>
                </li>

                <ul class="dropdown-menu" v-if="showMenu">
                    <li v-for="option in options">
                        <a href="javascript:void(0)" @click="updateOption(option)">
                            {{ option.name }}
                        </a>
                    </li>
                </ul>
            </div>
         `
    })

    var Station = Backbone.Model.extend({
      url: API_SERVER + '/api/stations',
      parse: function (response) {
        return {
          'id5': response.id5,
          'name': response.id5 + ' ' + response.name
        };
      }
    });
    var Stations = Backbone.Collection.extend({
      model: Station,
      url: API_SERVER + '/api/stations',
      parse: function(response){
        return response;
      }
    });

    var Variable = Backbone.Model.extend({
      url: API_SERVER + '/api/variables',
      parse: function (response) {
        return {
          'name': response.variable_name,
        };
      }
    });
    var Variables = Backbone.Collection.extend({
      model: Variable,
      url: API_SERVER + '/api/variables',
      parse: function(response){
        return response;
      }
    });


    // fetch collections and fill out dropDown lists
    var allStations = new Stations();
    var allVariables = new Variables();
    allStations.fetch().done(function() {
        allVariables.fetch().done(function() {
             new Vue({
                el: '#timelines-dropdowns',
                data: {
                    dropdowndatas: [
                        {
                            id: "variable-dropdown",
                            opts: allVariables.toJSON(),
                            placeholder: "Select the variable",
                            selectionAttr: "variable"
                        },
                        {
                            id: "station-dropdown",
                            opts: allStations.toJSON(),
                            placeholder: "Select the station",
                            selectionAttr: "station"
                        }
                    ]
                }
            });
        });
    });


    var Measurement = Backbone.Model.extend({
      url: API_SERVER + '/api/measurements',
      parse: function (response) {
        return {
          'date': response.date,
          'value': response.value
        };
      }
    });
    var Measurements = Backbone.Collection.extend({
      model: Measurement,
      url: API_SERVER + '/api/measurements',
      parse: function(response){
        return response;
      }
    });




    Vue.component('apexchart', VueApexCharts);

    var chartComponent = new Vue({
      methods: {
        resetData: function (dataSeries, station, variable_name) {
            var values = _.map(dataSeries, function(d){
                if(d.value == -999)
                    return null;
                else
                    return d.value;
            });
            var dates = _.map(dataSeries, function(d){return new Date(d.date);});
            var datas = [];
            for (var i = 0; i < dataSeries.length; i++) {
              if(values[i] != null)
                datas.push([dates[i], values[i]]);
            }
            if (datas.length == 0 && dataSeries.length > 0) {
                this['series']=[];
                this['chartOptions']={};
                alert("No reasonable data to present!")
                return;
            }
            this['series'] =
            [{
              name: variable_name,
              data: datas
            }];
            this['chartOptions'] =
            {
              chart: {
                stacked: false,
                zoom: {
                  type: 'x',
                  enabled: true
                },
                toolbar: {
                  autoSelected: 'zoom'
                }
              },
              plotOptions: {
                line: {
                  curve: 'smooth',
                }
              },
              dataLabels: {
                enabled: false
              },

              markers: {
                size: 0,
                style: 'full',
              },
              title: {
                text: 'Station ' + station.name,
                align: 'left'
              },
              fill: {
                type: 'gradient',
                gradient: {
                  shadeIntensity: 1,
                  inverseColors: false,
                  opacityFrom: 0.5,
                  opacityTo: 0,
                  stops: [0, 90, 100]
                },
              },
              yaxis: {
                min: Math.min.apply(null, values),
                max: Math.max.apply(null, values),
                labels: {
                  formatter: function (val) {
                     return val.toFixed(1);
                  },
                },
                title: {
                  text: 'Value'
                },
              },
              xaxis: {
                type: 'datetime',
                min: new Date(Math.min.apply(null, dates)),
                max: new Date(Math.max.apply(null, dates)),
                labels: {
                  formatter: function (date) {
                    var dateObj = new Date(date);
                    var mn = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    return dateObj.getDate() + " " + mn[dateObj.getMonth()] + " " + dateObj.getFullYear();
                  }
                }
              },

              tooltip: {
                shared: false,
                y: {
                  formatter: function (val) {
                    return val;
                  }
                }
              }
            };
        }
      },
      el: '#timelines-chart',
      data: {series:[], chartOptions:{}}
    });


    var TimelinesView = Backbone.View.extend({
        el: $('#timelines-chart'),
        initialize: function() {
            this.listenTo(selection, 'change', this.updateOptionCallback);
        },
        updateOptionCallback: function() {
            if (selection.get('variable') != null && selection.get('station') != null) {
                var measurements = new Measurements();
                  $.ajax({url: API_SERVER + '/api/measurements/' + selection.get('station').id5 + '/' + selection.get('variable').name,
                  success: function(result){
                    chartComponent.resetData(result, selection.get('station'), selection.get('variable').name);
                  }});
                this.render();
            }
            else {
                chartComponent.resetData([], {name: ""}, "");
            }
        }
    });

    var timelinesView = new TimelinesView();

});