using System;

namespace Crystal.Api.Services;

public class LogFormatter
{
    public string FormatEvent(string eventName, string module)
    {
        if (string.IsNullOrEmpty(eventName) || string.IsNullOrEmpty(module))
            throw new ArgumentException("Faltan datos del evento");

        return $"[{module.ToUpper()}] - EVENT: {eventName}";
    }
}