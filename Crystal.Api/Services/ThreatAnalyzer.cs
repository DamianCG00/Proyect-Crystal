namespace Crystal.Api.Services;

public class ThreatAnalyzer
{
    public string EvaluateSeverity(int threatLevel)
    {
        if (threatLevel >= 8) return "CRITICAL";
        if (threatLevel >= 5) return "WARNING";
        return "LOW";
    }
}