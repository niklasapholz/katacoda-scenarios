Dieses Kadacoda soll als Beispiel dienen, wie Daten von IoT-Geräten in eine relationale Datenbanken übertragen werden können.

In diesem Fall werden FIT-Daten verwendet, die bereits in JSON-Format umgewandelt wurden.

Das FIT-Protokoll wird häufig genutzt um Fitnessdaten zu speichern. So wird es zum Beispiel von Garmin und Zwift verwendet um Daten zu exportieren. Das Protokoll wird genauer beschrieben unter https://developer.garmin.com/fit/protocol/. In dieser Übung soll es nur um die bereits geparsten Daten, da das Parsen zu viel Aufwand wäre.

Die FIT-Dateien stammen meistens von Wearables, wie zum Beispiel Smartwatches oder Fitnesstracker, bzw. deren Sensoren. Diese arbeiten mit "Messwertaufnahme[n] für nichtelektrische Größen und bilden diese in eine elektrische Größe ab" (vgl. Buckenhofer-IOT02-Datenquellen - Folie 9).