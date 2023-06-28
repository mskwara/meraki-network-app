# Meraki Network Monitoring

## **Przypadki użycia**:
* ### **Heavy Hitters:**

    **Opis:**

    Aplikacja wyświetla 10 urządzeń, dla których zanotowano największą ilość wysłanych i odebranych pakietów,
wraz z podaniem konkretnych wartości.

    **Działanie:**
    * Wykorzystujemy funkcjonalności `Ruch sieciowego urządzeń` i `Obciążenie`
    * Wykonujemy zapytania z `Obciążenia` w celu uzyskania informacji, jak bardzo była obciążona sieć w czasie
    * Na podstawie odpowiedzi z poprzedniego zapytania 

* ### **Monitoring opóźnienia:**

  **Opis:**

  Aplikacja wyświetla opóźnienie sieci dla urządzeń znajdujących się w sieci w ramach połączenia z danym IP.

  **Działanie:**
    * Na początek wysyłamy request na endpoint `api/v1/organizations/{ORGANIZATION_ID}/devices`, aby uzyskać informację o urządzeniach obecnych w organizacji. Z uzyskanej odpowiedzi uzyskujemy `serial` dla każdego urządzenia czyli ich unikalne identyfikatory.
    * Następnie dla każdego z urządzeń wysyłamy request na endpoint `/api/v1/devices/{serial}/lossAndLatencyHistory` wykorzystując wcześniej wspomniany identyfikator do uzyskania informacji o straconych pakietach.
    * Na podstawie otrzymanych danych tworzymy wykres straconych pakietów od czasu.

* ### **Monitoring zgubionych pakietów:**

    **Opis:**

    Aplikacja wyświetla stosunek utraconych pakietów oraz krótkookresowe wahania sieci dla urządzeń znajdujących się w sieci w ramach połączenia z danym IP. 

    **Działanie:**
    * Na początek wysyłamy request na endpoint `api/v1/organizations/{ORGANIZATION_ID}/devices`, aby uzyskać informację o urządzeniach obecnych w organizacji. Z uzyskanej odpowiedzi uzyskujemy `serial` dla każdego urządzenia czyli ich unikalne identyfikatory.
    * Następnie dla każdego z urządzeń wysyłamy request na endpoint `/api/v1/devices/{serial}/lossAndLatencyHistory` wykorzystując wcześniej wspomniany identyfikator do uzyskania informacji o opóźnieniach oraz wahaniach dla połączeń z danym urządzeniem. Dodatkowo do żądania przekazujemy parametr `ip`,
    który określa, że interesują nas jedynie połączenia ze wspomnianym `ip`. 
    * Dzięki temu posiadamy informację o tym jaki procent pakietów nie docierał do odbiorcy oraz wahań w stanie połączenia tylko z tym `ip`.
    * w celu uzyskania historii zgubionych pakietów w danej sieci oraz krótkookresowych odchyleń w ostatnich 24 godzinach dla urządzeń znajdu
    * Na podstawie otrzymanych danych tworzymy wykres procentu straconych danych [`%`] wraz z przebiegiem czasu oraz wahań stanu połączenia.

* ### **Obciążenie:**

    **Opis:**

    Aplikacja wyświetla procentowe obciążenie sieci w poszczególnych godzinach w ciągu wybranego dnia.

    **Działanie:**
    * Wysyłamy request na endpoint `/api/v1/networks/{network_id}/clients/bandwidthUsageHistory` z parametrem `network_id`
    w celu uzyskania historii zużycia przepustowości w danej sieci w ostatnich 24 godzinach
    * Na podstawie otrzymanych danych tworzymy wykres zużycia przepustowości od czasu

* ### **Ruch sieciowy urządzeń:**
    **Opis:**

    Aplikacja wyświetla 10 urządzeń, dla których zanotowano w podanej godzinie (+20 min) największą ilość wysłanych
    i odebranych pakietów, wraz z podaniem konkretnych wartości.

    **Działanie:**
    * Wysyłamy request na endpoint `/api/v1/organizations/{ORGANIZATION_ID}/devices` z parametrem `networkIds[]` ustawionym jako identyfikator sieci w celu uzyskania
    wszystkich urządzeń z danej sieci
    * Dla wszystkich urządzeń z odpowiedzi wysyłamy zapytanie na endpoint `/api/v1/devices/{serial}/clients`, gdzie `serial` jest identyfikatorem urządzenia w celu otrzymania, wszystkich urządzeń klienckich, dla które były podpięte do sieci przez to urządzenie. Jako odpowiedź otrzymujemy liczbę pakietów wysłanych, oraz odebranych dla poszczególnych rządzeń klienckich 

* ### **Statystyki VPN:**
    **Opis:**

    Aplikacja wyświetla informację dla 10 najbardziej aktywnych peerów (z dostępnymi połączeniami VPN) o łącznej ilości wysłanych/odebranych danych w kilobajtach [`kb`] w ramach danej sieci. Zakres czasu, z którego dane powinny być wzięte pod uwagę można określić przez parametry `t0` oraz `t1` (data początkowa i końcowa) w parametrach zapytania.

    **Działanie:**
    * Wysyłamy request na endpoint `/organizations/{organizationId}/appliance/vpn/stats`, gdzie `organizationId` to unikalny identyfikator danej organizacji. Jako parametry żądania określamy:
      * `t0` - Data określająca początek zakresu czasu, dla którego statystyki są brane pod uwagę
      * `t1` - Data określająca koniec zakresu czasu, dla którego statystyki są brane pod uwagę
      * `networkId` - Identyfikator sieci, dla której analizujemy ruch VP
    * Zapytanie zwraca listę sieci organizacji z włączonymi połączeniami VPN, gdzie w naszym przypadku będzie to jedyna siec z `networkId` podanym na początku. Następnie
    Dla każdej takiej sieci jest również zwracana lista peer'ów (własność `merakiVPNPeers`) wykorzystywanych przy połączeniach VPN, gdzie każdy peer posiada informację o 
    wysłanych danych `sendInKilobytes` oraz odebranych danych `receivedInKilobytes` w kilobajtach [`kB`].

 

## **Opis wykorzystywanych zapytań**

### **`get` Devices**

Endpoint: `api/v1/organizations/{ORGANIZATION_ID}/devices`

[Dokumentacja](https://developer.cisco.com/meraki/api-latest/#!list-the-devices-in-an-organization)

### **`get` Loss and Latency History**

Endpoint: `/api/v1/devices/{serial}/lossAndLatencyHistory`

[Dokumentacja](https://developer.cisco.com/meraki/api-latest/#!get-the-uplink-loss-percentage-and-latency-in-milliseconds-and-goodput-in-kilobits-per-second-for-a-wired-network-device)

### **`get` Bandwidth Usage History**

Endpoint: `/api/v1/networks/{network_id}/clients/bandwidthUsageHistory`

[Dokumentacja](https://developer.cisco.com/meraki/api-latest/#!returns-a-timeseries-of-total-traffic-consumption-rates-for-all-clients-on-a-network-within-a-given-timespan-in-megabits-per-second)

### **`get` VPN Stats**

Endpoint: `/organizations/{organizationId}/appliance/vpn/stats`

[Dokumentacja](https://developer.cisco.com/meraki/api-latest/#!show-vpn-history-stat-for-networks-in-an-organization)

### **`get` Clients**

Endpoint: `/api/v1/devices/{serial}/clients`

[Dokumentacja](https://developer.cisco.com/meraki/api-latest/#!list-the-clients-of-a-device-up-to-a-maximum-of-a-month-ago)
