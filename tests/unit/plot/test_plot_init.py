from unittest.mock import Mock, patch

from six import StringIO

import pybloqs.plot as pp


def test_add_highcharts_shim_to_stream():
    highcharts_all = ["hc", "hc-module", "hc-pybloqs"]
    stream = StringIO()

    def side_effect(name):
        content = "PYBLOQS_SCRIPT" if name == "hc-pybloqs" else "SCRIPT"
        return Mock(content_string=content)

    with patch("pybloqs.static.JScript") as mock_jscript:
        mock_jscript.side_effect = side_effect
        pp.add_highcharts_shim_to_stream(stream, highcharts_all)

    result = stream.getvalue()
    expected = """
    <script type='text/javascript'>
         if (typeof require !== 'undefined') {
             
             require.undef("highcharts/hc");
             define('highcharts/hc', function(require, exports, module) {
                 SCRIPT 
             });
             
             require.undef("highcharts/hc_module");
             define('highcharts/hc_module', function(require, exports, module) {
                 SCRIPT 
             });
             
             require(['highcharts/hc', 'highcharts/hc_module'], function(hc, hc_module) { 
                 Highcharts = hc;
                 hc_module(Highcharts);
                 PYBLOQS_SCRIPT
                 window.Highcharts = Highcharts;
             });
         } 
     </script>
    """  # noqa E501
    # Using split() strips away all whitespace
    assert result.split() == expected.split()
