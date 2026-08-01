using Xunit;
using Crystal.Api.Services;

namespace Crystal.Tests;

public class ThreatAnalyzerTests
{
    [Fact]
    public void EvaluateSeverity_ConNivelAlto_RetornaCritical()
    {
        // 1. Arrange
        var analyzer = new ThreatAnalyzer();
        int nivelAmenaza = 9;

        // 2. Act
        var resultado = analyzer.EvaluateSeverity(nivelAmenaza);

        // 3. Assert
        Assert.Equal("CRITICAL", resultado);
    }
}