
/**
 * @brief Tablle für die Umrechnung von Batteriespannung in Prozent
 * richtet nach an einen S1 Lipo Akku mit einer Spannung von 3.7V
 * Richtet sich an diese Tabelle: https://blog.ampow.com/lipo-voltage-chart/
 * Ein Wert enthält die Spanne von 5 Prozent
 * 
 */
const float BATTERY_VOLTAGE_1S[] = {
    4.2, 4.15, 4.11, 4.08, 4.02, 3.98, 3.95, 3.91, 3.87, 3.85,
    3.84, 3.82, 3.8, 3.79, 3.77, 3.75, 3.73, 3.71, 3.69, 3.61, 3.27
};