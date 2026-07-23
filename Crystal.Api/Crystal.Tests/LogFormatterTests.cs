using Xunit;
using Crystal.Api.Services;

namespace Crystal.Tests;

public class LogFormatterTests
{
    [Fact]
    public void FormatEvent_ConDatosValidos_RetornaCadenaFormateada()
    {
        // 1. Arrange
        var formatter = new LogFormatter();
        string evento = "Intrusión detectada";
        string modulo = "Paladin";

        // 2. Act
        var resultado = formatter.FormatEvent(evento, modulo);

        // 3. Assert
        Assert.Equal("[PALADIN] - EVENT: Intrusión detectada", resultado);
    }
}