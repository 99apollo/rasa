# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import mysql.connector
class ActionFindLibrary(Action):
    def name(self) -> Text:
        return "action_find_libaray"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 여기에 도서관을 찾는 로직을 구현합니다.
        # 예를 들어, 사용자의 입력에서 도서관 이름을 추출하고 데이터베이스에서 검색하는 등의 작업이 이루어집니다.
        print("ActionFindLibrary run")
        # 'library_name'이라는 엔터티를 추출합니다.
        library_name = next(tracker.get_latest_entity_values("library_name"), "unknown")
        
        if library_name=="unknown":
            dispatcher.utter_message(f"sorry i can not understand please reenter library")
            return[SlotSet("current_story_complete", True)]
        
        # 추출된 엔터티를 슬롯에 저장합니다.
        tracker.slots["library_name_slot"] = library_name

        dispatcher.utter_message(f"Searching for information about {library_name}.")
        dispatcher.utter_message(f"what do you want to do? i can do finding books, borrowing books, table info, renting table, event info, event add")
        if library_name!="main" and library_name!="law" :
            library_name="all"
        return [SlotSet("library_name_slot",library_name)]

class ActionFindLibraryTable(Action):
    def name(self) -> Text:
        return "action_find_libaray_table"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 여기에 도서관을 찾는 로직을 구현합니다.
        # 예를 들어, 사용자의 입력에서 도서관 이름을 추출하고 데이터베이스에서 검색하는 등의 작업이 이루어집니다.
        print("ActionFindLibraryTable run")
        # 'library_name'이라는 엔터티를 추출합니다.
        library_name = next(tracker.get_latest_entity_values("library_name"), "unknown")
        
        if library_name!="main" and library_name!="law" :
            library_name="all"
        
        # 추출된 엔터티를 슬롯에 저장합니다.
        tracker.slots["library_name_slot"] = library_name

        dispatcher.utter_message(f"Searching for information about {library_name}.")
        return [SlotSet("library_name_slot",library_name)]


class ActionFindBookInfoSelected(Action):
    def name(self) -> Text:
        return "action_find_book_info_selected"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 여기에 선택된 도서에 대한 정보를 찾는 로직을 구현합니다.
        # 예를 들어, 사용자의 입력에서 도서 이름을 추출하고 데이터베이스에서 검색하는 등의 작업이 이루어집니다.
        print("ActionFindBookInfoSelected run")
        # 'book_name'이라는 엔터티를 추출합니다.
        book_title = next(tracker.get_latest_entity_values("book_name_search"), "unknown")
        
        # 저장된 도서관 이름 가져오기
        library_name = tracker.get_slot("library_name_slot")
        
        
        if library_name=="all" or library_name=="none" or library_name=="null":
            # MySQL 서버에 연결
            connection1 = mysql.connector.connect(
                host="localhost",
                user="root",
                password="apollo~1207",
                database="library"
            )
            try:
                cursor2=connection1.cursor()
                cursor2.execute(f"SELECT * FROM book WHERE book_name = '{book_title}'")
                result2 = cursor2.fetchone()
                if result2:
                    check="Not available for rent"
                    if result2[4]==1:
                        check="available for rent"
                    dispatcher.utter_message(f"Book found: Book ID:{result2[0]}, Book name: {result2[1]}, writer: {result2[2]}, location: {result2[3]}, rent: {check}")
                else:
                    dispatcher.utter_message(f"No information found for the book: {book_title} in {library_name} library.")
            finally:
                connection1.close()
  
        else :
            # MySQL 서버에 연결
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="apollo~1207",
                database="library"
            )
            try:
                cursor = connection.cursor()

                # 도서관과 책 이름을 이용하여 MySQL에서 데이터 조회
                query = f"SELECT * FROM {library_name} WHERE book_name = '{book_title}'"
                cursor.execute(query)

                # 조회 결과 가져오기
                result = cursor.fetchone()

                if result:
                    # 도서 정보 출력
                    cursor1=connection.cursor()
                    book_id = result[1]
                    cursor1.execute(f"SELECT * FROM book WHERE book_ID = {book_id}")
                    result1=cursor1.fetchone()
                    check="Not available for rent"
                    if result1[4]==1:
                        check="available for rent"
                    dispatcher.utter_message(f"Book found: Book ID:{result1[0]}, Book name: {result1[1]}, writer: {result1[2]}, location: {result1[3]}, rent: {check}")
                else:
                    # 도서가 없는 경우
                    dispatcher.utter_message(f"No information found for the book: {book_title} in {library_name} library.")

            finally:
                # 연결 종료
                connection.close()
                
        dispatcher.utter_message(f"Searching for information about the book: {book_title} in {library_name} library.")
        dispatcher.utter_message(f"this is the end of finding book. thank you for using us.")
        # 도서 정보를 가져와서 dispatcher.utter_message로 출력하거나,
        # 필요에 따라 slot에 저장할 수 있습니다.
        return []

class ActionFindBookBorrowSelected(Action):
    def name(self) -> Text:
        return "action_find_book_borrow_selected"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 'book_name_rent'이라는 엔터티를 추출합니다.
        print("ActionFindBookBorrowSelected run")
        book_title = next(tracker.get_latest_entity_values("book_name_borrow"), "unknown")
        
        # 저장된 도서관 이름 가져오기
        library_name = tracker.get_slot("library_name_slot")
        
        if library_name == "all":
            # MySQL 서버에 연결
            dispatcher.utter_message(f"if you want to rent a book, you have to select library first! ")
            """
            connection1 = mysql.connector.connect(
                host="localhost",
                user="root",
                password="apollo~1207",
                database="library"
            )
            try:
                cursor2 = connection1.cursor()
                cursor2.execute(f"SELECT * FROM book WHERE book_name = '{book_title}'")
                result2 = cursor2.fetchone()
                if result2:
                    if result2[4] == 1:
                        # 도서가 빌려지지 않은 상태인 경우
                        cursor2.execute(f"UPDATE book SET book_rental = 0 WHERE book_ID = {result2[0]}")
                        dispatcher.utter_message(f"The book '{book_title}' is now rented.")
                    else:
                        # 이미 빌려진 도서인 경우
                        dispatcher.utter_message(f"The book '{book_title}' is already rented.")
                else:
                    dispatcher.utter_message(f"No information found for the book: {book_title} in {library_name} library.")
            finally:
                connection1.close()
            """
        else:
            # MySQL 서버에 연결
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="apollo~1207",
                database="library"
            )
            try:
                cursor = connection.cursor()

                # 도서관과 책 이름을 이용하여 MySQL에서 데이터 조회
                query = f"SELECT * FROM {library_name} WHERE book_name = '{book_title}'"
                cursor.execute(query)

                # 조회 결과 가져오기
                result = cursor.fetchone()

                if result:
                    # 도서 정보 출력
                    cursor1 = connection.cursor()
                    book_id = result[1]
                    cursor1.execute(f"SELECT * FROM book WHERE book_ID = {book_id}")
                    result1 = cursor1.fetchone()
                    if result1[4] == 1:
                        cursor3=connection.cursor()
                        # 도서가 빌려지지 않은 상태인 경우
                        cursor3.execute(f"UPDATE book SET book_rental = 0 WHERE book_ID = {book_id}")
                        connection.commit()
                        dispatcher.utter_message(f"The book '{book_title}' in {library_name} library is now rented.")
                    else:
                        # 이미 빌려진 도서인 경우
                        dispatcher.utter_message(f"The book '{book_title}' in {library_name} library is already rented.")
                else:
                    # 도서가 없는 경우
                    dispatcher.utter_message(f"No information found for the book: {book_title} in {library_name} library.")

            finally:
                dispatcher.utter_message(f"this is the end of renting book. thank you for using us.")
                # 연결 종료
                connection.close()
        
        return []


class ActionGetTableInformation(Action):
    def name(self) -> Text:
        return "action_get_table_information"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 여기에 테이블 정보를 얻는 로직을 구현합니다.
        # 테이블에 관련된 정보를 데이터베이스에서 조회하거나 다른 소스에서 가져오는 등의 작업이 이루어집니다.
        print("ActionGetTableInformation run")       
        library_name = tracker.get_slot("library_name_slot")
        connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="apollo~1207",
                database="library"
        )
        try:
            cursor = connection.cursor()

            if library_name == "all":
                # 전체 도서관의 테이블 정보 조회
                cursor.execute("SELECT * FROM `library`.`table`")
            else:
                # 특정 도서관의 테이블 정보 조회
                cursor.execute(f"SELECT * FROM `library`.`table` WHERE `table_library` = '{library_name}'")

            # 조회 결과 가져오기
            table_info = cursor.fetchall()

            if table_info:
                # 테이블 정보 출력
                for row in table_info:
                    dispatcher.utter_message(f"Table ID: {row[0]}, Library: {row[1]}, Floor: {row[2]}, Table seat: {row[3]}, Available: {'Yes' if row[4] == 1 else 'No'}")
            else:
                # 테이블이 없는 경우
                dispatcher.utter_message(f"No table information found for {library_name} library.")

        finally:
            # 연결 종료
            connection.close()

        return []
    
class ActionGetTableRent(Action):
    def name(self) -> Text:
        return "action_get_table_rent"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 여기에 테이블 렌트 정보를 얻는 로직을 구현합니다.
        # 테이블 렌트에 관련된 정보를 데이터베이스에서 조회하거나 다른 소스에서 가져오는 등의 작업이 이루어집니다.
        print("ActionGetTableRent run")    
        library_name = tracker.get_slot("library_name_slot")
        table_floor = tracker.get_slot("table_floor_slot")
        table_seat = tracker.get_slot("table_seat_slot")
        if table_floor=="unknown":
            dispatcher.utter_message(f"enter table floor first!")
            return [SlotSet("table_seat_slot", table_seat)]
        # MySQL 서버에 연결
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="apollo~1207",
            database="library"
        )
        
        try:
            cursor = connection.cursor()

            if library_name == "all":
                dispatcher.utter_message(f"select library first!")
                return [SlotSet("table_seat_slot", table_seat)]
            else:
                # 특정 도서관의 테이블 정보 조회
                ##UPDATE book SET book_rental = 0 WHERE book_ID = {book_id}
                cursor.execute(f"UPDATE `library`.`table` SET `table_available` = 0 WHERE `table_library` = '{library_name}' AND `table_floor` = '{table_floor}' AND `table_number` = {table_seat}")
                connection.commit()
            
            # 업데이트된 테이블 정보 조회
            cursor.execute(f"SELECT * FROM `library`.`table` WHERE `table_library` = '{library_name}' AND `table_floor` = '{table_floor}' AND `table_number` = {table_seat}")
            updated_table_info = cursor.fetchall()

            if updated_table_info:
                # 테이블 렌트 정보 출력
                for row in updated_table_info:
                    dispatcher.utter_message(f"Table ID: {row[0]}, Library: {row[1]}, Floor: {row[2]}, Table seat: {row[3]} is currently rented.")
            else:
                # 대여 중인 테이블이 없는 경우
                dispatcher.utter_message(f"No rented table information found for {library_name} library on floor {table_floor} and table seat {table_seat}.")

        finally:
            # 연결 종료
            connection.close()

        return [SlotSet("table_seat_slot", table_seat)]


class ActionTableFloor(Action):
    def name(self) -> Text:
        return "action_table_floor"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 여기에 테이블 층수에 관한 로직을 구현합니다.
        # 테이블이 어느 층에 위치하는지 데이터베이스에서 조회하거나 다른 소스에서 가져오는 등의 작업이 이루어집니다.
        intent = tracker.latest_message['intent'].get('name')
        print(f"인식된 의도: {intent}")
        print("ActionTableFloor run")     
        table_floor = next(tracker.get_latest_entity_values("table_floor"), "unknown")
        library_name = tracker.get_slot("library_name_slot")
        # 예시: 테이블 층수 정보를 가져와서 dispatcher를 통해 출력
        if library_name=="all":
            dispatcher.utter_message(f"select library first!")
            return []
        dispatcher.utter_message(f"Table floor information: {table_floor}")


        return [SlotSet("table_floor_slot",table_floor)]


class ActionTableSeat(Action):
    def name(self) -> Text:
        return "action_table_seat"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 여기에 테이블 층수에 관한 로직을 구현합니다.
        # 테이블이 어느 층에 위치하는지 데이터베이스에서 조회하거나 다른 소스에서 가져오는 등의 작업이 이루어집니다.
        intent = tracker.latest_message['intent'].get('name')
        print(f"인식된 의도: {intent}")
        print("ActionTableSeat run")     
        table_seat = next(tracker.get_latest_entity_values("table_seat_number"), "unknown")
        library_name = tracker.get_slot("library_name_slot")
        # 예시: 테이블 층수 정보를 가져와서 dispatcher를 통해 출력
        if library_name=="all":
            dispatcher.utter_message(f"select library first!")
            return []
        dispatcher.utter_message(f"Table seat information: {table_seat}")
        dispatcher.utter_message(f"Do you confirm?")

        return [SlotSet("table_seat_slot",table_seat)]

# class ActionGetTableRent(Action):
#     def name(self) -> Text:
#         return "action_get_table_rent"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # 여기에 테이블 렌트 정보를 얻는 로직을 구현합니다.
#         # 테이블 렌트에 관련된 정보를 데이터베이스에서 조회하거나 다른 소스에서 가져오는 등의 작업이 이루어집니다.
#         print("ActionGetTableRent run")    
#         library_name = tracker.get_slot("library_name_slot")
#         table_floor = next(tracker.get_latest_entity_values("table_floor"), "unknown")
#         table_seat = next(tracker.get_latest_entity_values("table_seat_number"), "unknown")
#         if table_floor=="unknown":
#             dispatcher.utter_message(f"enter table floor first!")
#             return []
#         # MySQL 서버에 연결
#         connection = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="apollo~1207",
#             database="library"
#         )
        
#         try:
#             cursor = connection.cursor()

#             if library_name == "all":
#                 dispatcher.utter_message(f"select library first!")
#                 return []
#             else:
#                 # 특정 도서관의 테이블 정보 조회
#                 ##UPDATE book SET book_rental = 0 WHERE book_ID = {book_id}
#                 cursor.execute(f"UPDATE `library`.`table` SET `table_available` = 0 WHERE `table_library` = '{library_name}' AND `table_floor` = '{table_floor}' AND `table_number` = {table_seat}")
#                 connection.commit()
            
#             # 업데이트된 테이블 정보 조회
#             cursor.execute(f"SELECT * FROM `library`.`table` WHERE `table_library` = '{library_name}' AND `table_floor` = '{table_floor}' AND `table_number` = {table_seat}")
#             updated_table_info = cursor.fetchall()

#             if updated_table_info:
#                 # 테이블 렌트 정보 출력
#                 for row in updated_table_info:
#                     dispatcher.utter_message(f"Table ID: {row[0]}, Library: {row[1]}, Floor: {row[2]}, Table seat: {row[3]} is currently rented.")
#             else:
#                 # 대여 중인 테이블이 없는 경우
#                 dispatcher.utter_message(f"No rented table information found for {library_name} library on floor {table_floor} and table seat {table_seat}.")

#         finally:
#             # 연결 종료
#             connection.close()

#         return [SlotSet("table_seat_slot", table_seat), SlotSet("table_floor_slot",table_floor)]


class ActionEventUserID(Action):
    def name(self) -> Text:
        return "action_event_user_id"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Your custom action logic for event user ID
        user_id = tracker.get_slot("user_id")
        # Perform actions based on the user ID
        dispatcher.utter_message(text=f"User ID: {user_id}")

        return []
    
class ActionEventDate(Action):
    def name(self) -> Text:
        return "action_event_date"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Your custom action logic for event date
        event_date = tracker.get_slot("event_date")
        # Perform actions based on the event date
        dispatcher.utter_message(text=f"Event date: {event_date}")

        return []

class ActionEventAdd(Action):
    def name(self) -> Text:
        return "action_event_add"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Your custom action logic for adding events
        dispatcher.utter_message(text="Adding the event...")

        return []
    
class ActionEventName(Action):
    def name(self) -> Text:
        return "action_event_name"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Your custom action logic for event name
        event_name = tracker.get_slot("event_name")
        # Perform actions based on the event name
        dispatcher.utter_message(text=f"Event name: {event_name}")

        return []
    
class ActionEventInfo(Action):
    def name(self) -> Text:
        return "action_event_info"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Your custom action logic for providing event information
        dispatcher.utter_message(text="Here is the information about the event...")

        return []