Skan został wykonany dla aplikacji w języku Java:

![Zadanie 3 - Skan Java](https://github.com/PW-user/task2/assets/150120897/14605079-044a-47a5-9925-4a903a51c94d)

![Zadanie 3 - Skan Java 2](https://github.com/PW-user/task2/assets/150120897/7a24b021-6b76-4976-9a7f-d7eb7331ef36)

![Zadanie 3 - Koniec skanu Java](https://github.com/PW-user/task2/assets/150120897/27b03618-81e6-418b-9225-3cba7e5e1ab2)

Wyniki skanu:

![Zadanie 3 - Podatności Java](https://github.com/PW-user/task2/assets/150120897/b1bce58a-1dc4-42f0-a819-fa0500f5935a)

Podatność CRITICAL dla getobject:

![Zadanie 3 - CRITICAL vulnerability](https://github.com/PW-user/task2/assets/150120897/8bc16b0a-36cf-4063-ab5a-4fc1696e0d06)

W pakiecie getobject, w wersji 0.1.0, wykryto podatność Denial of Service, która może również prowadzić do podatności Remote Code Execution, oznaczonej jako podatność krytyczna. Funkcja posiada wadę przy zwracaniu obiektu, który nie jest walidowany co przyczynia się do wyżej podanej podatności. Zalecane jest zaktualizowanie do wersji minimum 1.0.0 (najnowsza 1.1.1).

Miejsce błędu:
- https://github.com/cowboy/node-getobject/blob/aba04a8e1d6180eb39eff09990c3a43886ba8937/lib/getobject.js#L48

Advisor:
- https://www.mend.io/vulnerability-database/CVE-2020-28282
