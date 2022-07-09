import pymysql
from project.config import host, user, password, db_name

try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
    )
    print('successfully connected... ')
    print("#" * 20)

    select_bid = """SELECT client_number as client, 
                                    SUM(outcome = "win") as win, 
                                    SUM(outcome = "lose") AS lose 
                            FROM bid
                            INNER JOIN event_value
                            ON bid.play_id = event_value.play_id
                            GROUP BY client_number; """

    select_event_entity = """
                            SELECT least(home_team, away_team) AS A, 
                                    greatest(home_team, away_team) AS B, 
                                    COUNT(*)
                            FROM event_entity
                            GROUP BY A, B
                            HAVING COUNT(*) >= 1
                            ORDER BY A, B 
                                """


    def connect_sql(sql: str) -> list:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()


    result = connect_sql(select_bid)

    print('| id Пользователя |', 'Ставка сыграла |', 'Поражение |')
    print('')
    for n, win, lose in result:
        print(f"|    {n}             |       {win}      |     {lose}")
    print('----------------------------------')
    result = connect_sql(select_event_entity)
    print('-------Всего игр между друг другом----------')

    for game1, game2, res in result:

        s = f"|{game1} {game2}"
        len_s = len(s)
        print(f" Первая команда: {game1}  Вторая команда: {game2}   Общих встреч : {res}")

except Exception as ex:
    print('connection Error')
    print(ex)