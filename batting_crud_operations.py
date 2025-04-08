from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError, OperationFailure
from typing import Dict, List, Union


batting_drills = {
    "assessment_id":1001,
    "user_id":None,
    "player_details":{
        "player_name":"Vihaan chaudhary",
        "player_age":12,
        "player_gender":"male",
        "arm":"",
        "academy_name":"Master Class Cricket Club"
    },
    "drill_metrics":
                {
                "top_hand":{
                        "drill_id":"JGVEXNdpWe7gQ4xZSHTe",
                        "main_path":"https://drive.google.com/file/d/1OchnKtHCOoVy5qLRIeLTMR2r44y6sNiF/view?usp=drive_link",
                        "return_direction_path":"https://drive.google.com/file/d/14BJuFOWsPNAXHl4C3SSsMeM69ApBz8pg/view?usp=drive_link",
                        "percentile":73,
                        "grade":"B+",
                        "insights":{
                            "ball_insights": ['Good', 'Good', 'Bad', 'Bad', 'Good', 'Good'],
                            "ball_comments": ['Accurate: Outside Off Stump Ball Hit to Cover.', 'Accurate: Outside Off Stump Ball Hit to Cover.', 'Inaccurate: Outside Off Stump Ball Hit to Square Leg.', 'Inaccurate: Off Stump Ball Hit to Cover.', 'Accurate: Outside Off Stump Ball Hit to Cover.', 'Accurate: Off Stump Ball Hit to Mid Off.']
                            },
                        "improvements":"Focus on improving shot selection and accuracy for off-stump deliveries by practicing targeted drills. Work on maintaining a consistent grip and stance, holding the bat slightly higher as in a match situation. ",
                        "drill_conducted":"13-02-2025",
                        "drill_qr_path":"https://drive.google.com/file/d/1uYPzXGTIeA-No39d4Avbdo6ccSWzHei0/view?usp=drive_link",
                        "coach_feedback":"Batters return direction of shots and control looks really good, batter needs to hold the bat from a little above like he would in a match and shoulder to lean on more for more power. "
                },
                "bottom_hand":{
                        "drill_id":"p1p6MTXmgVVpStfySF9M",
                        "main_path":"https://drive.google.com/file/d/1KPLS0Zs7OZlODKdqhETsHDJGBj3HIF_d/view?usp=drive_link",
                        "return_direction_path":"https://drive.google.com/file/d/1SNJrf15lc5sobKDakSvzogEyT_w7qALm/view?usp=drive_link",
                        "percentile":66,
                        "grade":"B",
                        "insights":{
                        "ball_insights": ['Good', 'Average', 'Average', 'Bad', 'Good', 'Average'],
                        "ball_comments": ['Accurate: Leg Stump Ball Hit to Mid On.', 'Inaccurate: Off Stump Ball Hit to Cover.', 'Inaccurate: Middle Stump Ball Hit to Mid On.', 'Inaccurate: Off Stump Ball Hit to Square Leg.', 'Accurate: Outside Off Stump Ball Hit to Cover.', 'Inaccurate: Off Stump Ball Hit to Cover.']
                        },
                        "improvements":"Focus on softening the bottom-hand grip to prevent bat face rotation, as noted by the coach. Practice off-stump deliveries to improve accuracy and direction, ensuring shots are played to Mid Off. Work on balance and alignment to maintain consistency across all delivery types.",
                        "drill_conducted":"13-02-2025",
                        "drill_qr_path":"https://drive.google.com/file/d/15P3APnmQR6KBkdOfFydBFJMrLGGqQMEW/view?usp=drive_link",
                        "coach_feedback":"Batter needs to hold the bottom hand much softer as the 3rd and 4th delivery ball went inside the line than through the line because of bat face turning at point of impact, othwerise the impact point is good and close to body."
                    },
                "power_hitting":{
                        "drill_id":"Ae9bDXU9ZCOb4wa8IIl0",
                        "img_1":"https://drive.google.com/file/d/13SL_PN_hYgJ317I-e6jQ1dM6NN1iSsHN/view?usp=drive_link",
                        "img_2":"https://drive.google.com/file/d/1OG2yjr9WVg3ilmRgzK-JmmBk_NiCVNen/view?usp=drive_link",
                        "percentile":88,
                        "grade":"A",
                        "insights":"The batter displays excellent bat speed for his age, with a peak of 82.43, indicating strong swing mechanics and power. However, fluctuations in ball speed suggest inconsistent energy transfer, which may impact shot effectiveness.",
                        "ball_metrics":{
                            "launch_angles":[32.75, 32.21, 16.66, 18.34, 15.36, 22.83],
                            "bat_speeds":[73.21, 66.32, 50.78, 70.65, 60.96, 82.43],
                            "ball_speeds_before":[16.01, 15.95, 15.93, 15.93, 17.07, 15.49],
                            "ball_speeds_after":[67.84, 59.43, 44.39, 61.18, 51.62, 71.23]
                            },
                        "improvements":"Refining weight transfer and timing will help maximize energy conversion, leading to more consistent power hitting. Focused drills on hip rotation and follow-through can further enhance shot efficiency and ball striking.",
                        "drill_conducted":"13-02-2025",
                        "drill_qr_path":"https://drive.google.com/file/d/1fDezWIIWoli5UaREzQVO0lTMZmsbIXI-/view?usp=drive_link",
                        "coach_feedback":"batter needs to keep his shoulder under the ball more to get more elevation as staying low is the key when lofting, also initial movement to be done before the ball comes close in the hitting arc"
                    },
                "hold_your_pose":{
                        "drill_id":"",
                        "img_1":"https://drive.google.com/file/d/1wSuYdV7RFBD1mtJvqhQ8AjT7Qk8iQsQB/view?usp=drive_link",
                        "img_2":"https://drive.google.com/file/d/1oM8AlqqASvHAWemVzhT9nh3nrKCtwyhF/view?usp=drive_link",
                        "img_3":"https://drive.google.com/file/d/1S2pz0BEVqOIleUMBGdhkc7xSEpkbre9J/view?usp=drive_link",
                        "img_4":"",
                        "img_5":"",
                        "img_6":"",
                        "percentile":70.2,
                        "grade":"C",
                        "insights":{
                            "ball_comments":[],
                            "ball_durations":[3.55, 3.62, 3.37]
                            },
                        "improvements":"To improve consistency in hold times, incorporating core stability drills will enhance endurance and post-shot balance. Strengthening lower-body stability with single-leg balance exercises can help sustain posture longer, leading to better overall shot control.",
                        "drill_conducted":"13-02-2025",
                        "drill_qr_path":"https://drive.google.com/file/d/1kwdrqynhr8fxF3At1fDnAenIhgvVFdPx/view?usp=drive_link",
                        "coach_feedback":"Beautiful balance when playing the drive, backfoot is perfectly on the toe showing great strength in nack leg, impact is good too. "
                    },
                "feet_planted":{
                        "drill_id":"",
                        "img_1":"https://drive.google.com/file/d/1IxdSDmvd75B0DuBxb2W41S9r664u5PZI/view?usp=drive_link",
                        "img_2":"https://drive.google.com/file/d/15kYlK29mvl0cMLTVqsUC6QiNud_l0lEk/view?usp=drive_link",
                        "img_3":"https://drive.google.com/file/d/1dvsyi_rMiWG5maYo2xR2xTYdRZidhIj7/view?usp=drive_link",
                        "img_4":"https://drive.google.com/file/d/1N_vqlQ7Qwj1nAB6fowaJJ3itfZyVyoPL/view?usp=drive_link",
                        "img_5":"https://drive.google.com/file/d/1T1pn5z7OyLP9FncjfudGohqqLtzSPGPT/view?usp=drive_link",
                        "img_6":"https://drive.google.com/file/d/1N7ZvprV6iizaLr41RjhSbVNDFQvLpHes/view?usp=drive_link",
                        "percentile":67,
                        "grade":"B",
                        "insights":{
                            "ball_comments": ["Average", "Good", "Good", "Average", "Good", "Average"],
                            "ball_insights": [
                                "Average Connection, Cover Drive, Feet Planted",
                                "Improper Feeding, Late Cut, Feet Planted",
                                "Good Connection, Off Drive, Feet Planted",
                                "Average Connection, Straight Drive, Feet Planted",
                                "Good Connection, Straight Shot, Feet Planted",
                                "Average Connection, Straight Drive, Feet Planted"
                            ]
                            },
                        "improvements":"Vihaan’s hands are moving well, and impact positioning is good. However, he should focus on playing more in the front V, ensuring the hands stay close to the body during the backlift. Consistently aligning shots in this direction will improve control and shot execution.",
                        "drill_conducted":"13-02-2025",
                        "drill_qr_path":"https://drive.google.com/file/d/1cR6JN2WmKY857wtPPTIJ83pRXNU764KO/view?usp=drive_link",
                        "coach_feedback":"Hands are moving well and impact is under the eyes whioch is good to see, try playing as much as possible in the front V direction keeping hands close to body when taking the backlift"
                    },
                "backfoot":{
                        "drill_id":"84BHNlDYZGQieB1jifAm",
                        "main_path":"https://drive.google.com/file/d/1ljVBrs_WnskYPgyOACBxs4I4sSF9hgWu/view?usp=drive_link",
                        "return_direction_path":"https://drive.google.com/file/d/1m8JQO0LGE-BqVF2m1OjxLtlLdJ-5ho9p/view?usp=drive_link",
                        "img_1":"https://drive.google.com/file/d/17TGZxgfcx-LnkBUQ7b50PbycDW-HfLaM/view?usp=drive_link",
                        "img_2":"https://drive.google.com/file/d/1dApCF-3piq3VU0aLzyLc5AueuzW0-oKn/view?usp=drive_link",
                        "img_3":"https://drive.google.com/file/d/1on-cnEqXWYYPxp1K-gNY8BU3FvjTZ_7L/view?usp=drive_link",
                        "img_4":"https://drive.google.com/file/d/1Vv8A4Y_vCQwDjFCdE-yV73oxx3Wc93oy/view?usp=drive_link",
                        "img_5":"https://drive.google.com/file/d/1zbNPucFfBX2nsO1nc2IUKCBbcv6n0RT1/view?usp=drive_link",
                        "img_6":"https://drive.google.com/file/d/1nAnIteDZ9APx056lVmw3TB0pMDaOUTlw/view?usp=drive_link",
                        "percentile":73,
                        "grade":"B+",
                        "insights":"The batter had mixed accuracy on the backfoot drive drill. Balls 2, 3, and 5 were accurate, but balls 1, 4, and 6 were not. Ball 6 scored 0, showing significant misexecution, particularly with leg and off stump deliveries.",
                        "improvements":"Focus on a side-on position, keeping hands closer to the body while driving. Practice alignment and balance for better shot direction, especially for leg and off stump deliveries. A consistent grip and stance will help avoid wide shots.",
                        "drill_conducted":"13-02-2025",
                        "drill_qr_path":"https://drive.google.com/file/d/1_oP9V2zupCjXVTTdMUyoHohGqtgtB_1L/view?usp=drive_link",
                        "drill_qr_path2":"https://drive.google.com/file/d/1pb4MI_sVL9v6-KfzI4JI6hPCXTf64pDH/view?usp=drive_link",
                        "coach_feedback":"hands are sometimes going wide away from the body while playing the drive, sideon position can be maintained better. Impact and direction drives look really good."
                    },
                "running_bw_wickets":{
                        "drill_id":"",
                        "img_1":"https://drive.google.com/file/d/1OTGpohvtWL4wWabkmN3a4d16p7OIlCUX/view?usp=drive_link",
                        "img_2":"https://drive.google.com/file/d/1Fbke27pqnvDqDWgeEFX0IxesIcXYLHsp/view?usp=drive_link",
                        "percentile":78,
                        "grade":"B+",
                        "run_time":11.88,
                        "avg_time":11,
                        "insights":"Vihaan completed the drill in 11.82 seconds, slightly above the 11-second baseline. His running is efficient, but a minor delay in acceleration after each run is affecting his overall time. Closing this gap will help him reach the target and improve his running between wickets.",
                        "improvements":"To reduce his time, Vihaan should focus on quick acceleration after each turn. Maintaining a low center of gravity, explosive first few steps, and strong arm drive will enhance speed. Sprint drills and interval training can help him develop better acceleration and reach the baseline target more consistently.",
                        "drill_conducted":"13-02-2025",
                        "drill_qr_path":"https://drive.google.com/file/d/1kSoTeZgtO0SzV-dUo-uxH9gVgMElYB_S/view?usp=drive_link",
                        "coach_feedback":"Batter is running well but needs to focus more on acceleration after completing a run as it will only reduce his running time"
                    }
                },
    "final_report_path":"",
    "overall_feedback":"",
    "overall_rating":None,
    "report_generated_date":None,
    "drill_date":None
}


class BattingDrillsCRUD:
    def __init__(self, uri: str, db_name: str = 'kpro', collection_name: str = 'drill_results'):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        
        # Create unique index on assessment_id if it doesn't exist
        self.collection.create_index([("assessment_id", ASCENDING)], unique=True)

    def create_document(self, document_data: Dict) -> Union[str, None]:
        """
        Inserts a new document into the collection.
        Validates required assessment_id and ensures uniqueness
        """
        if 'assessment_id' not in document_data:
            raise ValueError("Missing required field: assessment_id")
        
        try:
            result = self.collection.insert_one(document_data)
            return document_data['assessment_id']
        except DuplicateKeyError:
            print(f"Assessment ID {document_data['assessment_id']} already exists")
            return None
        except Exception as e:
            print(f"An error occurred while inserting document: {e}")
            return None

    def get_document(self, assessment_id: str) -> Union[Dict, None]:
        """Retrieves a document by its assessment_id"""
        try:
            return self.collection.find_one({"assessment_id": assessment_id})
        except Exception as e:
            print(f"Error retrieving document: {e}")
            return None

    def get_all_documents(self) -> List[Dict]:
        """Retrieves all documents in the collection"""
        try:
            return list(self.collection.find())
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []

    def update_document(self, assessment_id: str, updates: Dict) -> int:
        """
        Updates a document with specified updates using $set
        Supports nested fields using dot notation
        """
        try:
            result = self.collection.update_one(
                {"assessment_id": assessment_id},
                {"$set": updates}
            )
            return result.modified_count
        except DuplicateKeyError:
            print("Cannot update to duplicate assessment_id")
            return 0
        except OperationFailure as e:
            print(f"Operation failed: {e}")
            return 0
        except Exception as e:
            print(f"Error updating document: {e}")
            return 0

    def delete_document(self, assessment_id: str) -> int:
        """Deletes a document by its assessment_id"""
        try:
            result = self.collection.delete_one({"assessment_id": assessment_id})
            return result.deleted_count
        except Exception as e:
            print(f"Error deleting document: {e}")
            return 0

    def close_connection(self):
        """Closes the MongoDB connection"""
        self.client.close()

# Example Usage
if __name__ == "__main__":
    uri = "mongodb+srv://aman:N3cLLYBTrKMTElAS@kpro-staging.f3esdpg.mongodb.net/"

    # Initialize CRUD operations handler
    drills_crud = BattingDrillsCRUD(uri)

    # # Create a new document
    # new_drill = {
    #     "assessment_id": 1000,
    #     "drill_metrics": {
    #         "top_hand":{
    #                     "drill_id":None,
    #                     "main_path":"https://drive.google.com/file/d/1JeJMn7IyhTrflGiMqtVZ7PuU6xubMEt6/view?usp=drive_link",
    #                     "return_direction_path":"https://drive.google.com/file/d/1WNC4cgkTsvaaSZp_VUNiik8dsOkqrcde/view?usp=drive_link",
    #                     "percentile":43,
    #                     "grade":"C",
    #                     "insights":{
    #                         "ball_insights":['Bad', 'Average', 'Average', 'Bad', 'Good', 'Bad'],
    #                         "ball_comments":['Inaccurate: Middle Stump Ball Mistimed.', 'Inaccurate: Outside Off Stump Ball Hit to Mid Off.', 'Inaccurate: Middle Stump Ball Hit to Mid Off.', 'Inaccurate: Outside Off Stump Ball Hit to Square Leg.', 'Accurate: Outside Off Stump Ball Hit to Cover.', 'Inaccurate: Outside Off Stump Ball Hit to Square Leg.']
    #                     },
    #                     "improvements":"Focus on improving bat control and downswing technique to enhance accuracy. Practice drills that emphasize maintaining a controlled bat path and balanced stance. Work on shot selection by aligning the top hand grip correctly for off-stump deliveries, ensuring the ball is directed to the cover region. Strengthen the ability to judge the ball's line and length to avoid misdirecting off-stump deliveries to the leg side. Regular targeted practice will help develop consistency and precision in shot execution.",
    #                     "drill_conducted":"13-02-2025",
    #                     "drill_qr_path":"https://drive.google.com/file/d/1gch50wB2r0Elb8tgRuz1OhXwf58RsktZ/view?usp=drive_link",
    #                     "coach_feedback":"The athlete is not able to control the bat path and downswing to connect the ball hence most balls are missed or off stump balls are going towards leg stump."
    #             }
    #     }
    # }

    # # Create operation
    # assessment_id = drills_crud.create_document(batting_drills)
    # print(f"Created document with Assessment ID: {assessment_id}")

    # Read operation
    document = drills_crud.get_document(assessment_id=1001)
    print("Retrieved document:", document)
    # metric_name = "bottom_hand"
    # # Update operation
    # update_count = drills_crud.update_document(
    #     1000,
    #     {
    #         f"drill_metrics.{metric_name}": {
    #                     "drill_id":"XrJj8QhXuJjEg3dUhu7o",
    #                     "main_path":"https://drive.google.com/file/d/1E6-fR1LdpGXEuAZmzIuvvYmmkwUyVYiT/view?usp=drive_link",
    #                     "return_direction_path":"https://drive.google.com/file/d/16I43NasH7V9mMpgLRXPf8G-X8SmUgi9G/view?usp=drive_link",
    #                     "percentile":83,
    #                     "grade":"A",
    #                     "insights":{
    #                                 "ball_insights": ['Average', 'Average', 'Good', 'Good', 'Good', 'Good'],
    #                                 "ball_comments": ['Inaccurate: Off Stump Ball Hit to Cover.', 'Inaccurate: Off Stump Ball Hit to Cover.', 'Accurate: Outside Off Stump Ball Hit to Cover.', 'Accurate: Outside Off Stump Ball Hit to Cover.', 'Accurate: Outside Off Stump Ball Hit to Cover.', 'Accurate: Outside Off Stump Ball Hit to Cover.']
    #                                 },
    #                     "improvements":"To build on this progress, focus on maintaining consistent shot selection and accuracy from the start. Incorporate light bat drills to enhance stability and control, especially for off-stump deliveries. Emphasize proper grip alignment and balance to ensure precise placement. Regular practice with a focus on initial shot execution will help eliminate inaccuracies and improve overall performance.",
    #                     "drill_conducted":"13-02-2025",
    #                     "drill_qr_path":"https://drive.google.com/file/d/15P3APnmQR6KBkdOfFydBFJMrLGGqQMEW/view?usp=drive_link",
    #                     "coach_feedback":"Bottom hand stability is much better and most balls on off stump are being hit back in the right direction, however a light bat is suggested as the batter will get more stability to play along the ground"
    #                 }
    #     }
    # )
    # print(f"Updated {update_count} fields")

    # # Verify update
    # updated_doc = drills_crud.get_document(1000)
    # print("Updated document:", updated_doc)

    # # Delete operation
    # delete_count = drills_crud.delete_document(assessment_id)
    # print(f"Deleted {delete_count} documents")

    # Cleanup connection
    drills_crud.close_connection()