FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build

WORKDIR /src

COPY . .

# RUN dotnet restore "MyBlazorApp.csproj"

RUN dotnet build "MyBlazorApp.csproj" -c Release -o /app/build

RUN dotnet publish "MyBlazorApp.csproj" -c Release -o /app/public

FROM mcr.microsoft.com/dotnet/aspnet:8.0

WORKDIR /app

COPY --from=build /app/public .

ENTRYPOINT ["dotnet", "MyBlazorApp.dll", "--urls", "http://0.0.0.0:5000"]
