using Toybox.Test;
using Toybox.Lang;

(:test)
class HrTestSample {
    var heartRate;
    // Intentionally no timestamp: it is not required to read history HR.
    function initialize(rate) { heartRate = rate; }
}

(:test)
class HrTestIterator {
    var _rates as Lang.Array;
    var _index = 0;
    function initialize(rates) { _rates = rates; }
    function next() {
        if (_index >= _rates.size()) { return null; }
        var rate = _rates[_index];
        _index += 1;
        return new HrTestSample(rate);
    }
}

(:test)
class HrTestReader extends HeartRateReader {
    var _current;
    var _rates;
    var historyCalls = 0;
    function initialize(current, rates) {
        HeartRateReader.initialize();
        _current = current;
        _rates = rates;
    }
    function currentRate() { return _current; }
    function history() {
        historyCalls += 1;
        return _rates == null ? null : new HrTestIterator(_rates);
    }
}

(:test)
function hrCurrentTakesPriority(logger) {
    var reader = new HrTestReader(76, [66]);
    Test.assertEqual(reader.read(), 76);
    Test.assertEqual(reader.isHistory, false);
    Test.assertEqual(reader.historyCalls, 0);
    return true;
}

(:test)
function hrMissingTimestampStillReadsHistory(logger) {
    var reader = new HrTestReader(null, [72]);
    Test.assertEqual(reader.read(), 72);
    Test.assertEqual(reader.isHistory, true);
    return true;
}

(:test)
function hrSkipsInvalidNewestSamples(logger) {
    var reader = new HrTestReader(null, [255, null, 0, 68, 65]);
    Test.assertEqual(reader.read(), 68);
    Test.assertEqual(reader.isHistory, true);
    return true;
}

(:test)
function hrInvalidCurrentFallsBack(logger) {
    var reader = new HrTestReader(255, [74]);
    Test.assertEqual(reader.read(), 74);
    Test.assertEqual(reader.isHistory, true);
    return true;
}

(:test)
function hrNoDataStaysUnavailable(logger) {
    var reader = new HrTestReader(null, [255, 0, null]);
    Test.assert(reader.read() == null);
    Test.assertEqual(reader.isHistory, false);
    reader = new HrTestReader(null, null);
    Test.assert(reader.read() == null);
    return true;
}

(:test)
function hrOnlyExaminesTenSamples(logger) {
    var reader = new HrTestReader(null, [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 70]);
    Test.assert(reader.read() == null);
    return true;
}
