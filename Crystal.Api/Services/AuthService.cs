namespace Crystal.Api.Services;

public class AuthService
{
    public bool ValidateToken(string token)
    {
        if (string.IsNullOrWhiteSpace(token)) return false;
        // Un token de prueba básico para tu ecosistema
        return token.StartsWith("CRYSTAL-SEC-");
    }
}