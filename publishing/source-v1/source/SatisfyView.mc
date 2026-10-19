using Toybox.ActivityMonitor;
using Toybox.Graphics;
using Toybox.Math;
using Toybox.System;
using Toybox.Time;
using Toybox.Time.Gregorian;
using Toybox.WatchUi;

// FR45 runs Connect IQ 1.4.x and has a 48 KiB watch-face memory budget.
// Use small monochrome fonts and vector decoration instead of a full bitmap.
class SatisfyView extends WatchUi.WatchFace {
    var _timeFont;
    var _smallFont;
    var _nameFont;
    var _steps = null;
    var _goal = null;
    var _distance = null;
    var _calories = null;
    var _heartRate = null;
    var _lastRead = -1;

    function initialize() {
        WatchFace.initialize();
    }

    function onLayout(dc) {
        _timeFont = WatchUi.loadResource(Rez.Fonts.TimeFont);
        _smallFont = WatchUi.loadResource(Rez.Fonts.SmallFont);
        _nameFont = WatchUi.loadResource(Rez.Fonts.NameFont);
    }

    function onShow() {
        _lastRead = -1;
    }

    function onExitSleep() {
        _lastRead = -1;
    }

    function readMetrics(now) {
        // Avoid querying history every second while the watch is awake.
        if (_lastRead >= 0 && now >= _lastRead && now - _lastRead < 60) {
            return;
        }
        _lastRead = now;
        var info = ActivityMonitor.getInfo();
        _steps = info.steps;
        _goal = info.stepGoal;
        _distance = info.distance;
        _calories = info.calories;
        _heartRate = null;

        if (ActivityMonitor has :getHeartRateHistory) {
            var sample = ActivityMonitor.getHeartRateHistory(1, true).next();
            // A missing, invalid or old reading must not look like a live pulse.
            if (sample != null && sample.heartRate != null
                && sample.heartRate != ActivityMonitor.INVALID_HR_SAMPLE
                && sample.heartRate > 0 && sample.when != null) {
                var age = now - sample.when.value();
                if (age >= 0 && age <= 600) {
                    _heartRate = sample.heartRate;
                }
            }
        }
    }

    function numberText(value) {
        return value == null ? "--" : value.format("%d");
    }

    function drawText(dc, x, y, value, font) {
        dc.drawText(x, y, font, value, Graphics.TEXT_JUSTIFY_LEFT);
    }

    function onUpdate(dc) {
        var now = Time.now();
        readMetrics(now.value());
        var clock = System.getClockTime();
        var date = Gregorian.info(now, Time.FORMAT_SHORT);
        var days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];
        var hour = clock.hour;
        if (!System.getDeviceSettings().is24Hour) {
            hour = hour % 12;
            if (hour == 0) { hour = 12; }
        }

        dc.setColor(Graphics.COLOR_BLACK, Graphics.COLOR_WHITE);
        dc.clear();

        // Thin arc following the circular top edge, available on CIQ 1.x.
        var px = 35;
        var py = 33;
        for (var x = 36; x <= 173; x += 1) {
            var offset = x - 104;
            var y = (104 - Math.sqrt(99 * 99 - offset * offset)).toNumber();
            dc.drawLine(px, py, x, y);
            px = x;
            py = y;
        }

        var battery = System.getSystemStats().battery.toNumber();
        dc.drawRectangle(80, 18, 13, 7);
        dc.fillRectangle(93, 20, 2, 3);
        var batteryWidth = (9 * battery / 100.0).toNumber();
        if (batteryWidth > 0) { dc.fillRectangle(82, 20, batteryWidth, 3); }
        drawText(dc, 100, 15, battery.format("%d") + "%", _smallFont);

        var dateText = days[date.day_of_week - 1] + " " + date.day.format("%02d")
            + "." + date.month.format("%02d");
        drawText(dc, 30, 33, dateText, _smallFont);
        drawText(dc, 17, 49, hour.format("%02d") + ":" + clock.min.format("%02d"), _timeFont);
        drawText(dc, 149, 82, "SATISFY", _nameFont);

        var distanceText = "-- KM";
        if (_distance != null) {
            // ActivityMonitor distance is total daily distance in centimetres.
            distanceText = (_distance / 100000.0).format("%.1f") + " KM";
        }
        drawRow(dc, 97, "DIST", distanceText);
        drawRow(dc, 110, "STEPS", numberText(_steps));
        drawRow(dc, 123, "HEART RATE", numberText(_heartRate) + " BPM");
        // Recovery data requires API 3.3 and is unavailable on FR45.
        drawRow(dc, 136, "RECOVERY", "-- H");
        drawRow(dc, 149, "KCAL", numberText(_calories));

        var progress = null;
        if (_steps != null && _goal != null && _goal > 0) {
            progress = (_steps * 100.0 / _goal).toNumber();
        }
        drawWave(dc, progress);
    }

    function drawRow(dc, y, label, value) {
        drawText(dc, 24, y, label, _smallFont);
        // Leave a safe margin inside the curved edge for longer numbers.
        var font = _smallFont;
        var x = 149;
        if (dc.getTextWidthInPixels(value, font) > 49) { x = 140; }
        drawText(dc, x, y, value, font);
    }

    function drawWave(dc, progress) {
        var capped = progress == null ? 0 : progress;
        if (capped > 100) { capped = 100; }
        var lastX = 24;
        var lastY = 178;
        var cutoff = 24 + (160 * capped / 100.0).toNumber();
        for (var x = 24; x <= 184; x += 1) {
            var phase = (x - 24) * Math.PI / 160.0;
            var y = (178 - 15 * Math.sin(phase) * Math.sin(phase)).toNumber();
            dc.drawLine(lastX, lastY, x, y);
            // Dotted fill grows with the daily step goal, rather than fake data.
            if (x % 3 == 0 && x <= cutoff) {
                for (var dotY = y + 4; dotY < 206; dotY += 3) {
                    var dx = x - 104;
                    var dy = dotY - 104;
                    if (dx * dx + dy * dy < 102 * 102) {
                        dc.drawPoint(x, dotY);
                    }
                }
            }
            lastX = x;
            lastY = y;
        }
        var text = progress == null ? "--% GOAL" : progress.format("%d") + "% GOAL";
        var width = dc.getTextWidthInPixels(text, _smallFont);
        dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_WHITE);
        dc.fillRectangle(104 - width / 2 - 3, 183, width + 6, 14);
        dc.setColor(Graphics.COLOR_BLACK, Graphics.COLOR_WHITE);
        dc.drawText(104, 184, _smallFont, text, Graphics.TEXT_JUSTIFY_CENTER);
    }
}
