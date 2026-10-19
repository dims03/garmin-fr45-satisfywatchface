using Toybox.Activity;
using Toybox.ActivityMonitor;

// Prefer the current reading. FR45 firmware may expose only HR history.
// Keep its source explicit: a history reading is displayed as LAST HR.
class HeartRateReader {
    var isHistory = false;

    function initialize() {}

    function currentRate() {
        return Activity.getActivityInfo().currentHeartRate;
    }

    function history() {
        if (ActivityMonitor has :getHeartRateHistory) {
            return ActivityMonitor.getHeartRateHistory(10, true);
        }
        return null;
    }

    function validRate(rate) {
        return rate != null && rate > 0
            && rate != ActivityMonitor.INVALID_HR_SAMPLE;
    }

    function read() {
        isHistory = false;
        var rate = currentRate();
        if (validRate(rate)) { return rate; }

        var iterator = history();
        if (iterator == null) { return null; }
        // The latest slot can be invalid while the preceding slot is usable.
        // Do not require sample.when: some firmware omits this metadata.
        // A historical value is never presented as a current sensor reading.
        for (var count = 0; count < 10; count += 1) {
            var sample = iterator.next();
            if (sample == null) { break; }
            if (validRate(sample.heartRate)) {
                isHistory = true;
                return sample.heartRate;
            }
        }
        return null;
    }
}
