using Xunit;
using Crystal.Api.Services;

namespace Crystal.Tests;

public class AuthServiceTests
{
    [Fact]
    public void ValidateToken_ConTokenValido_RetornaTrue()
    {
        // 1. Arrange
        var authService = new AuthService();
        var token = "CRYSTAL-SEC-9999";

        // 2. Act
        var resultado = authService.ValidateToken(token);

        // 3. Assert
        Assert.True(resultado);
    }
}