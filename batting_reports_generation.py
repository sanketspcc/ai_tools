from fpdf import FPDF
from fpdf.fonts import FontFace
import math
import os

from groq import Groq


from batting_crud_operations import BattingDrillsCRUD


import requests
from urllib.parse import urlparse, parse_qs
import re


def generate_batting_drills_report(input_dict):

    bebasnue_regular_ttf = "fonts/BebasNeue-Regular.ttf"
    ppnueue_bold_otf = "fonts/ppneuemontreal-bold.otf"
    ppnueue_medium_otf = "fonts/ppneuemontreal-medium.otf"
    ppnueue_regular_ttf = "fonts/PPNeueMontreal-Regular.ttf"

    pdf = FPDF(orientation="L", unit="cm", format="A4")

    pdf.add_font("BebasNeue", style="", fname=bebasnue_regular_ttf)
    pdf.add_font("ppneuemontreal", style="B", fname=ppnueue_bold_otf)
    pdf.add_font("ppneuemontreal", style="", fname=ppnueue_medium_otf)
    pdf.add_font("ppneuemontreal", style="BI", fname=ppnueue_regular_ttf)

    KPro_Logo_red = "content/KPro_logo_red.jpg"
    KPro_Logo_white = "content/KPro_logo_white.png"
    # qr_code_text = input_dict['clips_qr_text']
    # qr_code = input_dict['clips_qr']
    # page3image1 = "/home/venku/new_batting_report/page3_image1.jpg"
    # page3image2 = "/home/venku/new_batting_report/page3_image2.png"


    ## Initial Page 1 ## 

    # Initial Page 1 Image
    initial_page_image = "content/page1.jpg"

    pdf.add_page()

    pdf.image(initial_page_image, 0, 0, 841.89/28.33, 595.28/28.33)

    ## Initial Page 2 ## 

    # Initial Page 2 Image
    initial_page_image = "content/page2.jpg"

    pdf.add_page()

    pdf.image(initial_page_image, 0, 0, 841.89/28.33, 595.28/28.33)


    ##First Page-----------------------------------------------------------------------------------------------------------------------


    pdf.add_page()

    pdf.set_fill_color(8,11,119)
    pdf.rect(x=76.01/28.33, y=0/28.33, w=235.25/28.33, h=pdf.h, style='F')

    pdf.image(KPro_Logo_red, 767.08/28.33, 12.66/28.33, 64.35/28.33, 26.33/28.33)

    # Function to draw a hexagon
    def draw_hexagon(pdf, x_center, y_center, side_length):
        pdf.set_draw_color(244, 244, 244)
        angle = 60  # degrees for a hexagon
        points = []
        for i in range(6):
            x = x_center + side_length * math.sin(math.radians(angle * i))
            y = y_center + side_length * math.cos(math.radians(angle * i))
            points.append((x, y))
        pdf.polygon(points)

    # Hexagon parameters
    x = 0.8  # Scale factor for hexagon size
    a, b = 20, pdf.h / 2  # Center coordinates of the hexagon
    player_name = 'Player'
    metrics_map = {
        'Metric1_median': 65,
        'Metric2_median': 60,
        'Metric3_median': 70,
        'Metric4_median': 60,
        'Metric5_median': 65,
        'Metric6_median': 55,
        'Metric1_player': input_dict.get('backfoot_percentile', 0),
        'Metric2_player': input_dict.get('hold_your_pose_percentile', 0),
        'Metric3_player': input_dict.get('running_bw_percentile', 0),
        'Metric4_player': input_dict.get('power_hitting_percentile', 0),
        'Metric5_player': input_dict.get('bottomhand_percentile', 0),
        'Metric6_player': input_dict.get('tophand_percentile', 0),
        'name': 'player'
    }

    # Convert metrics to lengths
    metric_lengths_median = [
        metrics_map[f'Metric{i}_median'] * 5 * x / 100 for i in range(1, 7)
    ]
    metric_lengths_player = [
        metrics_map[f'Metric{i}_player'] * 5 * x / 100 for i in range(1, 7)
    ]

    # Add concentric hexagons for scale
    for i in range(5):
        side_length = x * (i + 1)
        draw_hexagon(pdf, a, b, side_length)

    # Add scale lines and labels
    pdf.set_text_color(101, 101, 101)
    pdf.set_font('ppneuemontreal', '', 8.32)
    for i in [100, 80, 60, 40, 20]:
        pdf.text(a - .4, b - i * x / 20, f'{i}')

    # Coordinates of median scores
    median_coordinates = [
        (
            a + metric_lengths_median[i] * math.sin(math.radians(-60 * i)),
            b + metric_lengths_median[i] * math.cos(math.radians(-60 * i))
        ) for i in range(6)
    ]

    # Coordinates of player scores
    player_coordinates = [
        (
            a + metric_lengths_player[i] * math.sin(math.radians(-60 * i)),
            b + metric_lengths_player[i] * math.cos(math.radians(-60 * i))
        ) for i in range(6)
    ]

    # Red lines denoting player's scores
    pdf.set_draw_color(255, 113, 91)
    pdf.set_line_width(0.08)
    for i in range(6):
        pdf.line(a, b, player_coordinates[i][0], player_coordinates[i][1])
    pdf.set_line_width(0.02)

    # Violet hexagon denoting median scores
    with pdf.local_context(fill_opacity=0.2, stroke_opacity=0.5):
        pdf.set_fill_color(90, 44, 169)
        pdf.polygon(median_coordinates, 'DF')
    pdf.set_draw_color(90, 44, 169)
    pdf.polygon(median_coordinates)

    # Texts around the hexagon
    pdf.set_text_color(33, 33, 33)
    pdf.set_font('ppneuemontreal', '', 12.62)
    labels = ['Point of Contact', 'Balance', 'Running b/w Wickets', 'Power', 'Grip', 'Control']
    label_radius = 7 * x  # Larger radius for labels well outside the hexagon

    # Position labels directly along the vertex directions
    for i in range(6):
        # label_x = a + label_radius * math.sin(math.radians(-60 * i)) 
        label_x = 18.5 + label_radius * math.sin(math.radians(-60 * i)) 
        # label_y = b + label_radius * math.cos(math.radians(-60 * i))
        label_y = b + label_radius * math.cos(math.radians(-60 * i))
        pdf.text(label_x, label_y, labels[i])

    pdf.set_text_color(255,255,255)
    pdf.set_font("ppneuemontreal", "", 34)
    pdf.set_y(47.03/28.33)
    pdf.set_x(91.73/28.33)
    pdf.multi_cell(168.33/28.33, 35/28.33, "Batting Evaluation", 0, align='L')

    pdf.set_text_color(255,255,255)
    pdf.set_font("ppneuemontreal", "BI", 14)
    pdf.set_y(128.53/28.33)
    pdf.set_x(91.73/28.33)
    pdf.multi_cell(203.8/28.33, 160/28.33,f"KhiladiPro's visual AI technology, here's a detailed analysis of your cricket batting performance.\n\n{input_dict['skill_map_feedback']} ", 0,max_line_height=0.5,align='L')


    white = (255, 255, 255)
    blue = (8,11,119)
    headings_style = FontFace(color=blue, fill_color=white)

    # TABLE_DATA = (
    #     ("Sr No", "Name of test"),
    #     ("01", "Top hand drill"),
    #     ("02", "Bottom hand drill"),
    #     # ("03", "Feet planted drill"),
    #     # ("04", "Backfoot drive"),
    #     # ("05", "Backfoot defence"),
    #     # ("06", "Running b/w the wickets"),
    #     # ("07", "Hold your pose"),
    #     # ("08", "Point of contact"),
        
    # )

    # Dyamically Change 
    TABLE_DATA = (
        ("Sr No", "Name of test"),
    )
    table_content_counter = 1
    if input_dict['tophand']:
        TABLE_DATA += (("0" + str(table_content_counter), "Top hand drill"),)
        table_content_counter += 1
    if input_dict['bottomhand']:
        TABLE_DATA += (("0" + str(table_content_counter), "Bottom hand drill"),)
        table_content_counter += 1
    if input_dict['feetplanted']:
        TABLE_DATA += (("0" + str(table_content_counter), "Feet planted drill"),)
        table_content_counter += 1
    if input_dict['backfootdrive']:
        TABLE_DATA += (("0" + str(table_content_counter), "Backfoot drill"),)
        table_content_counter += 1
    if input_dict['power_hitting']:
        TABLE_DATA += (("0" + str(table_content_counter), "Power Hitting drill"),)
        table_content_counter += 1
    if input_dict['running_bw']:
        TABLE_DATA += (("0" + str(table_content_counter), "Running b/w the wickets"),)
        table_content_counter += 1
    if input_dict['hold_your_pose']:
        TABLE_DATA += (("0" + str(table_content_counter), "Hold your pose"),)
        table_content_counter += 1
    if input_dict['point_of_contact']:
        TABLE_DATA += (("0" + str(table_content_counter), "Point of contact"),)
        table_content_counter += 1
    

    
    pdf.set_y(400/28.33)
    pdf.set_x(91.73/28.33)
    pdf.set_fill_color(8,11,119)
    pdf.set_draw_color(255,255,255)
    pdf.set_font("ppneuemontreal","BI",8,)
    pdf.set_line_width(0.02)

    with pdf.table(
        headings_style=headings_style,
        width=7,
        col_widths=(1, 4),
        text_align="CENTER",
        align="LEFT",
    ) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    pdf.set_text_color(2,2,2)
    pdf.set_font("ppneuemontreal", "BI", 25)
    pdf.set_y(27.51/28.33)
    pdf.set_x(517.23/28.33)
    pdf.cell(109/28.33, 16/28.33, input_dict['month_of_assessment'], 0)

    pdf.set_text_color(0,0,0)
    pdf.set_font("ppneuemontreal", "", 17)
    pdf.set_y(501/28.33)
    pdf.set_x(395.76/28.33)
    pdf.cell(351/28.33, 12/28.33, f"{input_dict['player_name']}  |  {input_dict['player_gender']}  |  {input_dict['player_age']} Years  |  {input_dict['arm']}", 0)

    pdf.set_text_color(2,2,2)
    pdf.set_font("ppneuemontreal", "", 13)
    pdf.set_y(526/28.33)
    pdf.set_x(351.26/28.33)
    pdf.cell(440/28.33, 12/28.33, f"Academy: {input_dict['academy_name']}, Assessment Date: {input_dict['assessment_date']}", 0)      

    # insert grade
    grade = input_dict['overall_rating']   
        
    with pdf.local_context(fill_opacity=0.2):
            
            pdf.set_fill_color(254, 218, 217)
            start_x = 480/28.33
            start_y = 66.43/28.33
            side_val = 0.9
            gap_val = 1
            
            pdf.rect(start_x + 0*gap_val, start_y, side_val, side_val, round_corners=True, style="F")
            pdf.rect(start_x + 1*gap_val, start_y, side_val, side_val, round_corners=True, style="F")
            pdf.rect(start_x + 2*gap_val, start_y, side_val, side_val, round_corners=True, style="F")
            pdf.rect(start_x + 3*gap_val, start_y, side_val, side_val, round_corners=True, style="F")
            pdf.rect(start_x + 4*gap_val, start_y, side_val, side_val, round_corners=True, style="F")
            pdf.rect(start_x + 5*gap_val, start_y, side_val, side_val, round_corners=True, style="F")
            pdf.rect(start_x + 6*gap_val, start_y, side_val, side_val, round_corners=True, style="F")
            
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", size=18.39)
            grade_start_x = 0.01
            grade_start_xplus = 0.1
            
            pdf.set_y(0.2 + start_y)
            pdf.set_x(grade_start_x + start_x + 0*gap_val)
            pdf.cell(text = "A+")
            pdf.set_x(grade_start_xplus + start_x + 1*gap_val)
            pdf.cell(text = "A")
            pdf.set_x(grade_start_x + start_x + 2*gap_val)
            pdf.cell(text = "B+")
            pdf.set_x(grade_start_xplus + start_x + 3*gap_val)
            pdf.cell(text = "B")
            pdf.set_x(grade_start_x + start_x + 4*gap_val)
            pdf.cell(text = "C+")
            pdf.set_x(grade_start_xplus + start_x + 5*gap_val)
            pdf.cell(text = "C")
            pdf.set_x(grade_start_xplus + start_x + 6*gap_val)
            pdf.cell(text = "D")
        
    if grade == 'A+':
            with pdf.local_context(fill_opacity=1):
                pdf.set_fill_color(254, 218, 217)
                pdf.rect(start_x + 0*gap_val, start_y, side_val, side_val, round_corners=True, style="F")
                pdf.set_text_color(0,0,0)
                pdf.set_font("ppneuemontreal", size=18.39)
                pdf.set_x(grade_start_x + start_x + 0*gap_val)
                pdf.cell(text = "A+")
                
    elif grade == 'A':
            with pdf.local_context(fill_opacity=1):
                
                pdf.set_fill_color(254, 218, 217)
                pdf.rect(start_x + 1*gap_val, start_y, side_val, side_val, round_corners=True, style="F")
                pdf.set_text_color(0,0,0)
                pdf.set_font("ppneuemontreal", size=18.39)
                pdf.set_x(grade_start_x + start_x + 1*gap_val)
                pdf.cell(text = "A")
    elif grade == 'B+':
            with pdf.local_context(fill_opacity=1):
                
                pdf.set_fill_color(254, 218, 217)
                pdf.rect(start_x + 2*gap_val, start_y, side_val, side_val, round_corners=True, style="F")
                pdf.set_text_color(0,0,0)
                pdf.set_font("ppneuemontreal", size=18.39)
                pdf.set_x(grade_start_x + start_x + 2*gap_val)
                pdf.cell(text = "B+")
    elif grade == 'B':
            with pdf.local_context(fill_opacity=1):
                
                pdf.set_fill_color(254, 218, 217)
                pdf.rect(start_x + 3*gap_val, start_y, side_val, side_val, round_corners=True, style="F")
                pdf.set_text_color(0,0,0)
                pdf.set_font("ppneuemontreal", size=18.39)
                pdf.set_x(grade_start_x + start_x + 3*gap_val)
                pdf.cell(text = "B")
    elif grade == 'C+':
            with pdf.local_context(fill_opacity=1):
                pdf.set_text_color(0,0,0)
                pdf.set_fill_color(254, 218, 217)
                pdf.rect(start_x + 4*gap_val, start_y, side_val, side_val, round_corners=True, style="F")
                
                pdf.set_font("ppneuemontreal", size=18.39)
                pdf.set_x(grade_start_x + start_x + 4*gap_val)
                pdf.cell(text = "C+")
    elif grade == 'C':
            with pdf.local_context(fill_opacity=1):
                pdf.set_text_color(0,0,0)
                pdf.set_fill_color(254, 218, 217)
                pdf.rect(start_x + 5*gap_val, start_y, side_val, side_val, round_corners=True, style="F")
                
                pdf.set_font("ppneuemontreal", size=18.39)
                pdf.set_x(grade_start_x + start_x + 5*gap_val)
                pdf.cell(text = "C")
    elif grade == 'D':
            with pdf.local_context(fill_opacity=1):
                pdf.set_text_color(0,0,0)
                pdf.set_fill_color(254, 218, 217)
                pdf.rect(start_x + 6*gap_val, start_y, side_val, side_val, round_corners=True, style="F")
                
                pdf.set_font("ppneuemontreal", size=18.39)
                pdf.set_x(grade_start_x + start_x + 6*gap_val)
                pdf.cell(text = "D")

    ##Second Page-----------------------------------------------------------------------------------------------------------------------

    pdf.add_page()

    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(0, 0, 0)  # Black color for the border
    pdf.set_line_width(0.01)  # Adjust the width to make it very thin
    pdf.rect(x=0/28.33, y=65/28.33, w=840/28.33, h=196.85/28.33, style='FD', round_corners=True, corner_radius=0.1)

    pdf.set_font("ppneuemontreal", "", 34)
    pdf.set_y(80.85/28.33)
    pdf.set_x(42/28.33)
    pdf.cell(266/28.33, 52/28.33, "Batting Evaluation", 0)

    pdf.set_fill_color(8,11,119)
    pdf.rect(321.22/28.33, 80.85/28.33, 51.78/28.33, 51.78/28.33, "F",round_corners=True)

    pdf.set_text_color(255,255,255)
    pdf.set_font("ppneuemontreal", "BI", 29.59)
    pdf.set_y(90/28.33)
    pdf.set_x(329.22/28.33)
    pdf.cell(36/28.33, 36/28.33, input_dict['overall_rating'], 0)

    # pdf.image(qr_code, 474.05/28.33, 80.85/28.33, 50.95/28.33, 50.79/28.33)

    pdf.set_text_color(0,0,0)
    pdf.set_font("ppneuemontreal", "BI", 14)
    pdf.set_y(141.85/28.33)
    pdf.set_x(42/28.33)
    pdf.multi_cell(484.48/28.33, 112/28.33,input_dict['skill_map_feedback'], 0,max_line_height=0.5,align='L')


    #Top hand drill
    if input_dict['tophand']:
        pdf.set_fill_color(8,11,119)
        pdf.rect(40/28.33, 297.5/28.33, 343/28.33, 26/28.33, "F",round_corners=True)

        pdf.set_fill_color(255,255,255)
        pdf.rect(281/28.33, 300/28.33, 100/28.33, 21/28.33, "F",round_corners=True)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "B", 10)
        pdf.set_y(305/28.33)
        pdf.set_x(297/28.33)
        # pdf.cell(79/28.33, 11/28.33, "Percentile 72", 0)
        if input_dict['tophand_mistake']:
            pdf.cell(79/28.33, 11/28.33, f"    NA", 0)
        else:
            pdf.cell(79/28.33, 11/28.33, f"    {round(input_dict['tophand_percentile']/10, 1)}/10", 0)

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "BI", 14)
        pdf.set_y(297.5/28.33)
        pdf.set_x(52/28.33)
        pdf.cell(80/28.33, 26/28.33, "Top hand drill", 0)

        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(0, 0, 0)  # Black color for the border
        pdf.set_line_width(0.01)  # Adjust the width to make it very thin
        pdf.rect(x=40/28.33, y=323/28.33, w=343/28.33, h=35/28.33, style='FD', round_corners=True, corner_radius=0.1)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "BI", 10)
        pdf.set_y(328/28.33)
        pdf.set_x(49/28.33)
        pdf.multi_cell(335.05/28.33, 26/28.33,"The Top Hand Drill in cricket strengthens the top hand's control,\nenhancing shot stability, precision, and balance for better stroke play.", 0,max_line_height=0.5,align='L')

    if input_dict['bottomhand']:
        #Bottom hand drill
        pdf.set_fill_color(8,11,119)
        pdf.rect(40/28.33, 373.5/28.33, 343/28.33, 26/28.33, "F",round_corners=True)

        pdf.set_fill_color(255,255,255)
        pdf.rect(281/28.33, 376/28.33, 100/28.33, 21/28.33, "F",round_corners=True)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "B", 10)
        pdf.set_y(381/28.33)
        pdf.set_x(297/28.33)
        # pdf.cell(79/28.33, 11/28.33, "Percentile 89", 0)
        if input_dict['bottomhand_mistake']:
            pdf.cell(79/28.33, 11/28.33, f"    NA", 0)
        else:
            pdf.cell(79/28.33, 11/28.33, f"    {round(input_dict['bottomhand_percentile']/10, 1)}/10", 0)

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "BI", 14)
        pdf.set_y(373.5/28.33)
        pdf.set_x(52/28.33)
        pdf.cell(101/28.33, 26/28.33, "Bottom hand drill", 0)

        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(0, 0, 0)  # Black color for the border
        pdf.set_line_width(0.01)  # Adjust the width to make it very thin
        pdf.rect(x=40/28.33, y=399.5/28.33, w=343/28.33, h=35/28.33, style='FD', round_corners=True, corner_radius=0.1)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "BI", 10)
        pdf.set_y(404/28.33)
        pdf.set_x(49/28.33)
        pdf.multi_cell(325/28.33, 26/28.33,"Builds bottom-hand strength for added power and control,\nimproving bat speed and stroke execution, especially in aggressive shots.", 0,max_line_height=0.5,align='L')

    if input_dict['feetplanted']:
        #Feet planted drill
        pdf.set_fill_color(8,11,119)
        pdf.rect(40/28.33, 449.5/28.33, 343/28.33, 26/28.33, "F",round_corners=True)

        pdf.set_fill_color(255,255,255)
        pdf.rect(281/28.33, 452/28.33, 100/28.33, 21/28.33, "F",round_corners=True)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "B", 10)
        pdf.set_y(457/28.33)
        pdf.set_x(297/28.33)
        pdf.cell(79/28.33, 11/28.33, f"    {round(input_dict['feet_planted_percentile']/10, 1)}/10", 0)

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "BI", 14)
        pdf.set_y(449.5/28.33)
        pdf.set_x(52/28.33)
        pdf.cell(99/28.33, 26/28.33, "Feet planted drill", 0)

        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(0, 0, 0)  # Black color for the border
        pdf.set_line_width(0.01)  # Adjust the width to make it very thin
        pdf.rect(x=40/28.33, y=475.5/28.33, w=343/28.33, h=35/28.33, style='FD', round_corners=True, corner_radius=0.1)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "BI", 10)
        pdf.set_y(480/28.33)
        pdf.set_x(49/28.33)
        pdf.multi_cell(475.5/28.33, 26/28.33,"Improves balance and stability by ensuring a firm base,\nenabling precise shot execution and better adaptability to various deliveries.", 0,max_line_height=0.5,align='L')

    if input_dict['backfootdrive']:
        #Backfoot drill
        pdf.set_fill_color(8,11,119)
        pdf.rect(475/28.33, 297.5/28.33, 343/28.33, 26/28.33, "F",round_corners=True)

        pdf.set_fill_color(255,255,255)
        pdf.rect(716/28.33, 300/28.33, 100/28.33, 21/28.33, "F",round_corners=True)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "B", 10)
        pdf.set_y(305/28.33)
        pdf.set_x(726.5/28.33)
        if input_dict['backfoot_mistake']:
            pdf.cell(79/28.33, 11/28.33, f"    NA", 0)
        else:
            pdf.cell(79/28.33, 11/28.33, f"             {round(input_dict['backfoot_percentile']/10, 1)}/10", 0)

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "BI", 14)
        pdf.set_y(297.5/28.33)
        pdf.set_x(487/28.33)
        pdf.cell(78/28.33, 26/28.33, "Backfoot drill", 0)

        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(0, 0, 0)  # Black color for the border
        pdf.set_line_width(0.01)  # Adjust the width to make it very thin
        pdf.rect(x=475/28.33, y=323.5/28.33, w=343/28.33, h=35/28.33, style='FD', round_corners=True, corner_radius=0.1)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "BI", 10)
        pdf.set_y(328/28.33)
        pdf.set_x(484/28.33)
        pdf.multi_cell(325/28.33, 26/28.33,"Enhances backfoot play, focusing on balance and precision\nfor executing defensive and attacking shots against short deliveries. ", 0,max_line_height=0.5,align='L')

    if input_dict['power_hitting']:
        #Power hitting drill
        pdf.set_fill_color(8,11,119)
        pdf.rect(475/28.33, 373.5/28.33, 343/28.33, 26/28.33, "F",round_corners=True)

        pdf.set_fill_color(255,255,255)
        pdf.rect(716/28.33, 376/28.33, 100/28.33, 21/28.33, "F",round_corners=True)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "B", 10)
        pdf.set_y(381/28.33)
        pdf.set_x(726.5/28.33)
        pdf.cell(79/28.33, 11/28.33, f"             {round(input_dict['power_hitting_percentile']/10, 1)}/10", 0)

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "BI", 14)
        pdf.set_y(373.5/28.33)
        pdf.set_x(487/28.33)
        pdf.cell(102/28.33, 26/28.33, "Power hitting drill", 0)

        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(0, 0, 0)  # Black color for the border
        pdf.set_line_width(0.01)  # Adjust the width to make it very thin
        pdf.rect(x=475/28.33, y=399.5/28.33, w=343/28.33, h=35/28.33, style='FD', round_corners=True, corner_radius=0.1)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "BI", 10)
        pdf.set_y(404/28.33)
        pdf.set_x(484/28.33)
        pdf.multi_cell(325/28.33, 26/28.33,"Develops explosive batting power through proper body rotation and timing,\nboosting boundary-hitting ability and overall scoring potential.", 0,max_line_height=0.5,align='L')

    if input_dict['running_bw']:
        #Running b/w the wickets
        pdf.set_fill_color(8,11,119)
        pdf.rect(475/28.33, 449.5/28.33, 343/28.33, 26/28.33, "F",round_corners=True)

        pdf.set_fill_color(255,255,255)
        pdf.rect(716/28.33, 452/28.33, 100/28.33, 21/28.33, "F",round_corners=True)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "B", 10)
        pdf.set_y(457/28.33)
        pdf.set_x(726.5/28.33)
        pdf.cell(79/28.33, 11/28.33, f"             {round(input_dict['running_bw_percentile']/10, 1)}/10", 0)

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "BI", 14)
        pdf.set_y(449.5/28.33)
        pdf.set_x(487/28.33)
        pdf.cell(146/28.33, 26/28.33, "Running b/w the wickets", 0)

        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(0, 0, 0)  # Black color for the border
        pdf.set_line_width(0.01)  # Adjust the width to make it very thin
        pdf.rect(x=475/28.33, y=475.5/28.33, w=343/28.33, h=35/28.33, style='FD', round_corners=True, corner_radius=0.1)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "BI", 10)
        pdf.set_y(480/28.33)
        pdf.set_x(484/28.33)
        pdf.multi_cell(325/28.33, 26/28.33,"Refines speed, coordination, and decision-making,\noptimizing quick singles and converting runs efficiently during gameplay.", 0,max_line_height=0.5,align='L')

    ##Third Page-----------------------------------------------------------------------------------------------------------------------

    if input_dict['tophand']:

        pdf.add_page()

        pdf.set_fill_color(8,11,119)
        pdf.rect(0, 0, pdf.w, 3, 'F') # Changed

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "", 34)
        pdf.set_y(18/28.33) # Changed
        pdf.set_x(33.88/28.33)
        pdf.cell(197/28.33, 52/28.33, "Top hand drill", 0)

        if not input_dict['tophand_mistake']:
            pdf.set_fill_color(255,255,255)
            pdf.rect(277.88/28.33, 18/28.33, 51.78/28.33, 51.78/28.33, "F",round_corners=True) # Y Changed

            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "BI", 29.59)
            pdf.set_y(27/28.33) # Changed
            pdf.set_x(285.77/28.33)
            pdf.cell(36/28.33, 36/28.33, input_dict['tophand_rating'], 0)

        pdf.image(KPro_Logo_white, 661/28.33, 18/28.33) # Y Changed
        pdf.image(input_dict['tophand_qr'], 763/28.33, 18/28.33, 44/28.33, 44/28.33)

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "BI", 6)
        pdf.set_y(65/28.33)
        pdf.set_x(753/28.33)
        pdf.cell(53/28.33, 7/28.33, "Scan to view the video", 0)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 14)
        pdf.set_y(111/28.33)
        pdf.set_x(34/28.33)
        pdf.cell(85/28.33, 17/28.33, "Top hand drill", 0)

        # pdf.image("page3_image1.jpg", 34/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)
        pdf.image(input_dict['tophand_main'], 34/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)

        if input_dict['tophand_mistake']:
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "", 14)
            pdf.set_y(111/28.33)
            pdf.set_x(264.27/28.33)
            pdf.cell(115/28.33, 17/28.33, "Top hand drill Mistake", 0)

            # pdf.image("tophand3_return_direction.png", 264.27/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)
            pdf.image(input_dict['tophand_mistake'], 264.27/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)
        else:
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "", 14)
            pdf.set_y(111/28.33)
            pdf.set_x(264.27/28.33)
            pdf.cell(115/28.33, 17/28.33, "Top hand drill map", 0)

            # pdf.image("tophand3_return_direction.png", 264.27/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)
            pdf.image(input_dict['tophand_return_direction'], 264.27/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)

        # pdf.set_text_color(0,0,0)
        # pdf.set_font("ppneuemontreal", "BI", 12)
        # pdf.set_y(109.7/28.33)
        # pdf.set_x(517.94/28.33)
        # pdf.cell(82/28.33, 14/28.33, "Return direction", 0)

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "B", 14)
        pdf.set_y(111/28.33)
        pdf.set_x(518.62/28.33)
        pdf.cell(45/28.33, 14/28.33, "Insights:", 0)

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "BI", 13)
        # pdf.set_y(128.7/28.33)
        # pdf.set_x(518.62/28.33)
        # pdf.multi_cell(280/28.33, 14/28.33, f"                      {input_dict['tophand_insights']}", 0,max_line_height=0.5,align='L')
        
        box_y = 130

        pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
        pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(570/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, input_dict['tophand_ball_1'],0)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, "Ball 1",0) 

        pdf.set_y((box_y+2+18)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(272/28.33, 27/28.33, input_dict['tophand_ball_1_comment'], 0)

        box_y += 50

        pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
        pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(570/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, input_dict['tophand_ball_2'],0)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, "Ball 2",0) 

        # Ball Review Comment
        pdf.set_y((box_y+2+18)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(272/28.33, 27/28.33, input_dict['tophand_ball_2_comment'], 0)

        box_y += 50

        pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
        pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(570/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, input_dict['tophand_ball_3'],0)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, "Ball 3",0) 

        # Ball Review Comment
        pdf.set_y((box_y+2+18)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(272/28.33, 27/28.33, input_dict['tophand_ball_3_comment'], 0)

        box_y += 50

        pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
        pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(570/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, input_dict['tophand_ball_4'],0)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, "Ball 4",0) 

        # Ball Review Comment
        pdf.set_y((box_y+2+18)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(272/28.33, 27/28.33, input_dict['tophand_ball_4_comment'], 0)

        box_y += 50

        pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
        pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(570/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, input_dict['tophand_ball_5'],0)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, "Ball 5",0) 

        # Ball Review Comment
        pdf.set_y((box_y+2+18)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(272/28.33, 27/28.33, input_dict['tophand_ball_5_comment'], 0)

        box_y += 50

        pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
        pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(570/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, input_dict['tophand_ball_6'],0)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, "Ball 6",0) 

        # Ball Review Comment
        pdf.set_y((box_y+2+18)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(272/28.33, 27/28.33, input_dict['tophand_ball_6_comment'], 0)
        

        pdf.set_fill_color(255, 204, 21)
        pdf.rect(476.8/28.33, 440.64/28.33, 365.2/28.33, 179.36/28.33, 'F') # modified

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "B", 14)
        pdf.set_y(450/28.33)
        pdf.set_x(518.62/28.33)
        pdf.cell(45/28.33, 14/28.33, "Improvements:", 0)

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "BI", 11)
        pdf.set_y(470/28.33)
        pdf.set_x(518.62/28.33)
        pdf.multi_cell(300/28.33, 12/28.33, f"{input_dict['tophand_improvements']}", 0,max_line_height=0.5,align='L')


        #---------------------------------------------------------------------


    if input_dict['bottomhand']:
        ##Fourth Page-----------------------------------------------------------------------------------------------------------------------

        pdf.add_page()

        pdf.set_fill_color(8,11,119)
        pdf.rect(0, 0, pdf.w, 3, 'F')

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "", 34)
        pdf.set_y(18/28.33)
        pdf.set_x(33.88/28.33)
        pdf.cell(197/28.33, 52/28.33, "Bottom hand drill", 0)

        if not input_dict['bottomhand_mistake']:
            pdf.set_fill_color(255,255,255)
            pdf.rect(300/28.33, 18/28.33, 51.78/28.33, 51.78/28.33, "F",round_corners=True)

            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "BI", 29.59)
            pdf.set_y(27/28.33)
            pdf.set_x(308/28.33)
            pdf.cell(36/28.33, 36/28.33, input_dict['bottomhand_rating'], 0)

        pdf.image(KPro_Logo_white, 661/28.33, 18/28.33)

        pdf.image(input_dict['bottomhand_qr'], 763/28.33, 18/28.33, 44/28.33, 44/28.33)

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "BI", 6)
        pdf.set_y(65/28.33)
        pdf.set_x(753/28.33)
        pdf.cell(53/28.33, 7/28.33, "Scan to view the video", 0)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 14)
        pdf.set_y(111/28.33)
        pdf.set_x(34/28.33)
        pdf.cell(85/28.33, 17/28.33, "Bottom hand drill", 0)

        # pdf.image("page3_image1.jpg", 34/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)
        pdf.image(input_dict['bottomhand_main'], 34/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)
        
        if input_dict['bottomhand_mistake']:
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "", 14)
            pdf.set_y(111/28.33)
            pdf.set_x(264.27/28.33)
            pdf.cell(115/28.33, 17/28.33, "Bottom hand drill Mistake", 0)

            # pdf.image("page3_image2.jpg", 264.27/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)
            pdf.image(input_dict['bottomhand_mistake'], 264.27/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)

            pdf.set_text_color(2,2,2)
            pdf.set_font("ppneuemontreal", "B", 14)
            pdf.set_y(111/28.33)
            pdf.set_x(518.62/28.33)
            pdf.cell(45/28.33, 14/28.33, "Drill Mistake:", 0)

            pdf.set_text_color(2,2,2)
            pdf.set_font("ppneuemontreal", "BI", 11)
            pdf.set_y(141/28.33)
            pdf.set_x(518.62/28.33)
            pdf.multi_cell(300/28.33, 12/28.33, f"Unable to generate metrics, Batsman is playing lofted shots, please play on ground drives", 0,max_line_height=0.5,align='L')


        else:
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "", 14)
            pdf.set_y(111/28.33)
            pdf.set_x(264.27/28.33)
            pdf.cell(115/28.33, 17/28.33, "Bottom hand drill map", 0)

            # pdf.image("page3_image2.jpg", 264.27/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)
            pdf.image(input_dict['bottomhand_return_direction'], 264.27/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)

            # pdf.set_text_color(0,0,0)
            # pdf.set_font("ppneuemontreal", "BI", 12)
            # pdf.set_y(109.7/28.33)
            # pdf.set_x(517.94/28.33)
            # pdf.cell(82/28.33, 14/28.33, "Return direction", 0)

            pdf.set_text_color(2,2,2)
            pdf.set_font("ppneuemontreal", "B", 14)
            pdf.set_y(111/28.33)
            pdf.set_x(518.62/28.33)
            pdf.cell(45/28.33, 14/28.33, "Insights:", 0)

            # pdf.set_text_color(2,2,2)
            # pdf.set_font("ppneuemontreal", "BI", 13)
            # pdf.set_y(128.7/28.33)
            # pdf.set_x(518.62/28.33)
            # pdf.multi_cell(280/28.33, 14/28.33, f"                      {input_dict['bottomhand_insights']}", 0,max_line_height=0.5,align='L')

            box_y = 130

            pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
            pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(570/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, input_dict['bottomhand_ball_1'],0)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, "Ball 1",0) 

            pdf.set_y((box_y+2+18)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(272/28.33, 27/28.33, input_dict['bottomhand_ball_1_comment'], 0)

            box_y += 50

            pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
            pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(570/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, input_dict['bottomhand_ball_2'],0)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, "Ball 2",0) 

            # Ball Review Comment
            pdf.set_y((box_y+2+18)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(272/28.33, 27/28.33, input_dict['bottomhand_ball_2_comment'], 0)

            box_y += 50

            pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
            pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(570/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, input_dict['bottomhand_ball_3'],0)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, "Ball 3",0) 

            # Ball Review Comment
            pdf.set_y((box_y+2+18)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(272/28.33, 27/28.33, input_dict['bottomhand_ball_3_comment'], 0)

            box_y += 50

            pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
            pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(570/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, input_dict['bottomhand_ball_4'],0)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, "Ball 4",0) 

            # Ball Review Comment
            pdf.set_y((box_y+2+18)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(272/28.33, 27/28.33, input_dict['bottomhand_ball_4_comment'], 0)

            box_y += 50

            pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
            pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(570/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, input_dict['bottomhand_ball_5'],0)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, "Ball 5",0) 

            # Ball Review Comment
            pdf.set_y((box_y+2+18)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(272/28.33, 27/28.33, input_dict['bottomhand_ball_5_comment'], 0)

            box_y += 50

            # pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
            # pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
            # pdf.set_text_color(0,0,0)
            # pdf.set_font("ppneuemontreal", "",  12)
            # pdf.set_y((box_y+2)/28.33)
            # pdf.set_x(570/28.33)#+6
            # pdf.cell(24/28.33, 16/28.33, input_dict['bottomhand_ball_6'],0)
            # pdf.set_text_color(0,0,0)
            # pdf.set_font("ppneuemontreal", "",  12)
            # pdf.set_y((box_y+2)/28.33)
            # pdf.set_x(524/28.33)#+6
            # pdf.cell(24/28.33, 16/28.33, "Ball 6",0) 

            # # Ball Review Comment
            # pdf.set_y((box_y+2+18)/28.33)
            # pdf.set_x(524/28.33)#+6
            # pdf.cell(272/28.33, 27/28.33, input_dict['bottomhand_ball_6_comment'], 0)
            

            pdf.set_fill_color(255, 204, 21)
            pdf.rect(476.8/28.33, 440.64/28.33, 365.2/28.33, 179.36/28.33, 'F') # modified

            pdf.set_text_color(2,2,2)
            pdf.set_font("ppneuemontreal", "B", 14)
            pdf.set_y(450/28.33)
            pdf.set_x(518.62/28.33)
            pdf.cell(45/28.33, 14/28.33, "Improvements:", 0)

            pdf.set_text_color(2,2,2)
            pdf.set_font("ppneuemontreal", "BI", 11)
            pdf.set_y(470/28.33)
            pdf.set_x(518.62/28.33)
            pdf.multi_cell(300/28.33, 12/28.33, f"{input_dict['bottomhand_improvements']}", 0,max_line_height=0.5,align='L')



    if input_dict['feetplanted']:
        # ##Fifth Page-----------------------------------------------------------------------------------------------------------------------


        pdf.add_page()

        pdf.set_fill_color(8,11,119)
        pdf.rect(0, 0, pdf.w, 3, 'F')

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "", 34)
        pdf.set_y(18/28.33)
        pdf.set_x(33.88/28.33)
        pdf.cell(237/28.33, 52/28.33, "Feet Planted drill", 0)

        pdf.set_fill_color(255,255,255)
        pdf.rect(288.88/28.33, 18/28.33, 51.78/28.33, 51.78/28.33, "F",round_corners=True)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "BI", 29.59)
        pdf.set_y(27/28.33)
        pdf.set_x(296.77/28.33)
        pdf.cell(36/28.33, 36/28.33, input_dict['feet_planted_rating'], 0)

        pdf.image(KPro_Logo_white, 661/28.33, 18/28.33)

        pdf.image(input_dict['feet_planted_qr'], 763/28.33, 18/28.33, 44/28.33, 44/28.33)

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "BI", 6)
        pdf.set_y(65/28.33)
        pdf.set_x(753/28.33)
        pdf.cell(53/28.33, 7/28.33, "Scan to view the video", 0)


        #-------------------------------------------------------------------------------------------------
        # pdf.set_text_color(0,0,0)
        # pdf.set_font("ppneuemontreal", "", 10)
        # pdf.set_y(103.81/28.33)
        # pdf.set_x(34/28.33)
        # pdf.cell(62/28.33, 13/28.33, "Ball 1", 0)

        # # pdf.image(input_dict['hold_your_pose_1'], 33.88/28.33, 122.01/28.33, 286.75/28.33, 122.41/28.33)
        # pdf.image(input_dict['feet_planted_1'], 33.88/28.33, 122.01/28.33, 130/28.33, 200/28.33)

        # #-------------------------------------------------------------------------------------------------

        # pdf.set_text_color(0,0,0)
        # pdf.set_font("ppneuemontreal", "", 10)
        # pdf.set_y(103.81/28.33)
        # # pdf.set_x(336.62/28.33)
        # pdf.set_x(190/28.33)
        # pdf.cell(62/28.33, 13/28.33, "Ball 2", 0)

        # # pdf.image(input_dict['hold_your_pose_2'], 336.62/28.33, 122.01/28.33, 286.75/28.33, 122.41/28.33)
        # pdf.image(input_dict['feet_planted_2'], 190/28.33, 122.01/28.33, 130/28.33, 200/28.33)

        # #-------------------------------------------------------------------------------------------------

        # pdf.set_text_color(0,0,0)
        # pdf.set_font("ppneuemontreal", "", 10)
        # # pdf.set_y(262.5/28.33)
        # pdf.set_y(103.81/28.33)
        # # pdf.set_x(34/28.33)
        # pdf.set_x(340/28.33)
        # pdf.cell(62/28.33, 13/28.33, "Ball 3", 0)

        # # pdf.image(input_dict['hold_your_pose_3'], 33.38/28.33, 280.42/28.33, 286.75/28.33, 122.41/28.33)
        # pdf.image(input_dict['feet_planted_3'], 340/28.33, 122.01/28.33, 130/28.33, 200/28.33)

        # #-------------------------------------------------------------------------------------------------

        # pdf.set_text_color(0,0,0)
        # pdf.set_font("ppneuemontreal", "", 10)
        # # pdf.set_y(262.5/28.33)
        # pdf.set_y(330/28.33)
        # # pdf.set_x(336.62/28.33)
        # pdf.set_x(34/28.33)
        # pdf.cell(62/28.33, 13/28.33, "Ball 4", 0)

        # # pdf.image(input_dict['hold_your_pose_4'], 336.62/28.33, 280.42/28.33, 286.75/28.33, 122.41/28.33)
        # pdf.image(input_dict['feet_planted_4'], 33.88/28.33, 350/28.33, 130/28.33, 200/28.33)

        # #-------------------------------------------------------------------------------------------------

        # pdf.set_text_color(0,0,0)
        # pdf.set_font("ppneuemontreal", "", 10)
        # # pdf.set_y(421.19/28.33)
        # pdf.set_y(330/28.33)
        # # pdf.set_x(34/28.33)
        # pdf.set_x(190/28.33)
        # pdf.cell(62/28.33, 13/28.33, "Ball 5", 0)

        # # pdf.image(input_dict['hold_your_pose_5'], 33.38/28.33, 438.84/28.33, 286.75/28.33, 122.41/28.33)
        # pdf.image(input_dict['feet_planted_5'], 190/28.33, 350/28.33, 130/28.33, 200/28.33)

        # #-------------------------------------------------------------------------------------------------

        # pdf.set_text_color(0,0,0)
        # pdf.set_font("ppneuemontreal", "", 10)
        # # pdf.set_y(421.19/28.33)
        # pdf.set_y(330/28.33)
        # # pdf.set_x(336.62/28.33)
        # pdf.set_x(340/28.33)
        # pdf.cell(62/28.33, 13/28.33, "Ball 6", 0)

        # # pdf.image(input_dict['hold_your_pose_6'], 336.62/28.33, 438.84/28.33, 286.75/28.33, 122.41/28.33)
        # pdf.image(input_dict['feet_planted_6'], 340/28.33, 350/28.33, 130/28.33, 200/28.33)

        ## SIDE VIEW ## 
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 10)
        pdf.set_y(103.81/28.33)
        pdf.set_x(34/28.33)
        pdf.cell(62/28.33, 13/28.33, "Ball 1", 0)

        pdf.image(input_dict['feet_planted_1'], 33.88/28.33, 122.01/28.33, 210/28.33, 95/28.33)

        #-------------------------------------------------------------------------------------------------

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 10)
        pdf.set_y(103.81/28.33)
        pdf.set_x(265/28.33)
        pdf.cell(62/28.33, 13/28.33, "Ball 2", 0)

        pdf.image(input_dict['feet_planted_2'], 264/28.33, 122.01/28.33, 210/28.33, 95/28.33)

        #-------------------------------------------------------------------------------------------------

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 10)
        pdf.set_y(262.5/28.33)
        pdf.set_x(34/28.33)
        pdf.cell(62/28.33, 13/28.33, "Ball 3", 0)

        pdf.image(input_dict['feet_planted_3'], 33.38/28.33, 280.42/28.33, 210/28.33, 95/28.33)

        #-------------------------------------------------------------------------------------------------

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 10)
        pdf.set_y(262.5/28.33)
        pdf.set_x(265/28.33)
        pdf.cell(62/28.33, 13/28.33, "Ball 4", 0)

        pdf.image(input_dict['feet_planted_4'], 264/28.33, 280.42/28.33, 210/28.33, 95/28.33)

        #-------------------------------------------------------------------------------------------------

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 10)
        pdf.set_y(421.19/28.33)
        pdf.set_x(34/28.33)
        pdf.cell(62/28.33, 13/28.33, "Ball 5", 0)

        pdf.image(input_dict['feet_planted_5'], 33.38/28.33, 438.84/28.33, 210/28.33, 95/28.33)

        #-------------------------------------------------------------------------------------------------

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 10)
        pdf.set_y(421.19/28.33)
        pdf.set_x(265/28.33)
        pdf.cell(62/28.33, 13/28.33, "Ball 6", 0)

        pdf.image(input_dict['feet_planted_6'], 264/28.33, 438.84/28.33, 210/28.33, 95/28.33)


        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "B", 14)
        pdf.set_y(111/28.33)
        pdf.set_x(518.62/28.33)
        pdf.cell(45/28.33, 14/28.33, "Insights:", 0)

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "BI", 13)
        # pdf.set_y(128.7/28.33)
        # pdf.set_x(518.62/28.33)
        # pdf.multi_cell(280/28.33, 14/28.33, f"                      {input_dict['bottomhand_insights']}", 0,max_line_height=0.5,align='L')

        box_y = 130

        pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
        pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(570/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, input_dict['feet_planted_ball_1'],0)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, "Ball 1",0) 

        pdf.set_y((box_y+2+18)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(272/28.33, 27/28.33, input_dict['feet_planted_ball_1_comment'], 0)

        box_y += 50

        pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
        pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(570/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, input_dict['feet_planted_ball_2'],0)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, "Ball 2",0) 

        # Ball Review Comment
        pdf.set_y((box_y+2+18)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(272/28.33, 27/28.33, input_dict['feet_planted_ball_2_comment'], 0)

        box_y += 50

        pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
        pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(570/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, input_dict['feet_planted_ball_3'],0)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, "Ball 3",0) 

        # Ball Review Comment
        pdf.set_y((box_y+2+18)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(272/28.33, 27/28.33, input_dict['feet_planted_ball_3_comment'], 0)

        box_y += 50

        pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
        pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(570/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, input_dict['feet_planted_ball_4'],0)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, "Ball 4",0) 

        # Ball Review Comment
        pdf.set_y((box_y+2+18)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(272/28.33, 27/28.33, input_dict['feet_planted_ball_4_comment'], 0)

        box_y += 50

        pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
        pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(570/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, input_dict['feet_planted_ball_5'],0)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, "Ball 5",0) 

        # Ball Review Comment
        pdf.set_y((box_y+2+18)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(272/28.33, 27/28.33, input_dict['feet_planted_ball_5_comment'], 0)

        box_y += 50

        pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
        pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(570/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, input_dict['feet_planted_ball_6'],0)
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "",  12)
        pdf.set_y((box_y+2)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(24/28.33, 16/28.33, "Ball 6",0) 

        # Ball Review Comment
        pdf.set_y((box_y+2+18)/28.33)
        pdf.set_x(524/28.33)#+6
        pdf.cell(272/28.33, 27/28.33, input_dict['feet_planted_ball_6_comment'], 0)
        

        pdf.set_fill_color(255, 204, 21)
        pdf.rect(476.8/28.33, 440.64/28.33, 365.2/28.33, 179.36/28.33, 'F') # modified

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "B", 14)
        pdf.set_y(450/28.33)
        pdf.set_x(518.62/28.33)
        pdf.cell(45/28.33, 14/28.33, "Improvements:", 0)

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "BI", 11)
        pdf.set_y(470/28.33)
        pdf.set_x(518.62/28.33)
        pdf.multi_cell(300/28.33, 12/28.33, f"{input_dict['feet_planted_improvements']}", 0,max_line_height=0.5,align='L')


        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "B", 14)
        # pdf.set_y(130.19/28.33)
        # pdf.set_x(650/28.33)
        # pdf.cell(45/28.33, 14/28.33, "Insights:", 0)

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "BI", 13)
        # pdf.set_y(130.19/28.33)
        # pdf.set_x(650/28.33)
        # pdf.multi_cell(180/28.33, 48/28.33, f"                                   {input_dict['feet_planted_insights']}", 0,max_line_height=0.5,align='L')


        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "B", 14)
        # pdf.set_y(270/28.33)
        # pdf.set_x(650/28.33)
        # pdf.cell(45/28.33, 14/28.33, "Improvements:", 0)

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "BI", 13)
        # pdf.set_y(270/28.33)
        # pdf.set_x(650/28.33)
        # pdf.multi_cell(180/28.33, 14/28.33, f"                                    {input_dict['feet_planted_improvements']}", 0,max_line_height=0.5,align='L')


        # pdf.image(input_dict['feet_planted_qr'], 692/28.33, 436.81/28.33, 97.26/28.33, 124.95/28.33)


    if input_dict['backfootdefense']:
        ##Sixth Page-----------------------------------------------------------------------------------------------------------------------


        pdf.add_page()

        pdf.set_fill_color(8,11,119)
        pdf.rect(0, 0, pdf.w, 3, 'F')

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "", 34)
        pdf.set_y(18/28.33)
        pdf.set_x(33.88/28.33)
        pdf.cell(197/28.33, 52/28.33, "Backfoot drill", 0)

        
        if not input_dict['backfoot_mistake']:
            pdf.set_fill_color(255,255,255)
            pdf.rect(277.88/28.33, 18/28.33, 51.78/28.33, 51.78/28.33, "F",round_corners=True)

            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "BI", 29.59)
            pdf.set_y(27/28.33)
            pdf.set_x(285.77/28.33)
            pdf.cell(36/28.33, 36/28.33, input_dict['backfoot_rating'], 0)

        pdf.image(KPro_Logo_white, 573/28.33, 18/28.33)

        pdf.image(input_dict['backfoot_defense_qr'], 698/28.33, 18/28.33, 44/28.33, 44/28.33)

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "BI", 6)
        pdf.set_y(65/28.33)
        pdf.set_x(688/28.33)
        pdf.cell(53/28.33, 7/28.33, "Scan to view the video", 0)

        pdf.image(input_dict['backfoot_drive_qr'], 763/28.33, 18/28.33, 44/28.33, 44/28.33)

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "BI", 6)
        pdf.set_y(65/28.33)
        pdf.set_x(753/28.33)
        pdf.cell(53/28.33, 7/28.33, "Scan to view the video", 0)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 14)
        pdf.set_y(111/28.33)
        pdf.set_x(34/28.33)
        pdf.cell(85/28.33, 17/28.33, "Backfoot drive", 0)

        # pdf.image("page3_image1.jpg", 34/28.33, 133/28.33, 212.53/28.33, 424.1/28.33) 
        pdf.image(input_dict['backfoot_main'], 34/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)

        if input_dict['backfoot_mistake']:
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "", 14)
            pdf.set_y(111/28.33)
            pdf.set_x(264.27/28.33)
            pdf.cell(115/28.33, 17/28.33, "Backfoot drive Mistake", 0)

            pdf.image(input_dict['backfoot_mistake'], 264.27/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)

            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "", 14)
            pdf.set_y(111/28.33)
            pdf.set_x(513.89/28.33)
            pdf.cell(113/28.33, 17/28.33, "Backfoot defence", 0)

            pdf.image(input_dict['backfoot_defense1'], 513.89/28.33, 133/28.33, 50/28.33, 95/28.33)

            pdf.image(input_dict['backfoot_defense2'], 576.17/28.33, 133/28.33, 50/28.33, 95/28.33)

            pdf.image(input_dict['backfoot_defense3'], 638.45/28.33, 133/28.33, 50/28.33, 95/28.33)

            pdf.image(input_dict['backfoot_defense4'], 513.89/28.33, 235.15/28.33, 50/28.33, 95/28.33)

            pdf.image(input_dict['backfoot_defense5'], 576.17/28.33, 235.15/28.33, 50/28.33, 95/28.33)

            pdf.image(input_dict['backfoot_defense6'], 638.45/28.33, 235.15/28.33, 50/28.33, 95/28.33)

            pdf.set_text_color(2,2,2)
            pdf.set_font("ppneuemontreal", "B", 14)
            pdf.set_y(350/28.33)
            pdf.set_x(513/28.33)
            pdf.cell(45/28.33, 14/28.33, "Drill Mistake:", 0)

            pdf.set_text_color(2,2,2)
            pdf.set_font("ppneuemontreal", "BI", 11)
            pdf.set_y(375/28.33)
            pdf.set_x(514.62/28.33)
            pdf.multi_cell(300/28.33, 12/28.33, f"Unable to generate metrics, Batsman is playing lofted shots, please play on ground drives", 0,max_line_height=0.5,align='L')

        else:
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "", 14)
            pdf.set_y(111/28.33)
            pdf.set_x(264.27/28.33)
            pdf.cell(115/28.33, 17/28.33, "Backfoot drive map", 0)

            pdf.image(input_dict['backfoot_return_direction'], 264.27/28.33, 133/28.33, 212.53/28.33, 424.1/28.33)

            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "", 14)
            pdf.set_y(111/28.33)
            pdf.set_x(513.89/28.33)
            pdf.cell(113/28.33, 17/28.33, "Backfoot defence", 0)

            pdf.image(input_dict['backfoot_defense1'], 513.89/28.33, 133/28.33, 50/28.33, 95/28.33)

            pdf.image(input_dict['backfoot_defense2'], 576.17/28.33, 133/28.33, 50/28.33, 95/28.33)

            pdf.image(input_dict['backfoot_defense3'], 638.45/28.33, 133/28.33, 50/28.33, 95/28.33)

            pdf.image(input_dict['backfoot_defense4'], 513.89/28.33, 235.15/28.33, 50/28.33, 95/28.33)

            pdf.image(input_dict['backfoot_defense5'], 576.17/28.33, 235.15/28.33, 50/28.33, 95/28.33)

            pdf.image(input_dict['backfoot_defense6'], 638.45/28.33, 235.15/28.33, 50/28.33, 95/28.33)

            pdf.set_text_color(2,2,2)
            pdf.set_font("ppneuemontreal", "B", 14)
            pdf.set_y(350/28.33)
            pdf.set_x(513/28.33)
            pdf.cell(45/28.33, 14/28.33, "Insights:", 0)

            pdf.set_text_color(2,2,2)
            pdf.set_font("ppneuemontreal", "BI", 11)
            pdf.set_y(370/28.33)
            pdf.set_x(513/28.33)
            pdf.multi_cell(300/28.33, 12/28.33, f"{input_dict['backfoot_insights']}", 0,max_line_height=0.5,align='L')

            pdf.set_fill_color(255, 204, 21)
            pdf.rect(476.8/28.33, 440.64/28.33, 365.2/28.33, 179.36/28.33, 'F') # modified

            pdf.set_text_color(2,2,2)
            pdf.set_font("ppneuemontreal", "B", 14)
            pdf.set_y(450/28.33)
            pdf.set_x(513/28.33)
            pdf.cell(45/28.33, 14/28.33, "Improvements:", 0)

            pdf.set_text_color(2,2,2)
            pdf.set_font("ppneuemontreal", "BI", 11)
            pdf.set_y(470/28.33)
            pdf.set_x(513/28.33)
            pdf.multi_cell(300/28.33, 12/28.33, f"{input_dict['backfoot_improvements']}", 0,max_line_height=0.5,align='L')


        # pdf.set_text_color(0,0,0)
        # pdf.set_font("ppneuemontreal", "", 14)
        # pdf.set_y(133/28.33)
        # pdf.set_x(736.16/28.33)
        # pdf.cell(113/28.33, 17/28.33, "Drive Clips", 0)
        
        # pdf.image(input_dict['backfoot_drive_qr'], 736.16/28.33, 148/28.33, 70.26/28.33, 70.95/28.33)

        # pdf.set_text_color(0,0,0)
        # pdf.set_font("ppneuemontreal", "", 14)
        # pdf.set_y(235/28.33)
        # pdf.set_x(736.16/28.33)
        # pdf.cell(113/28.33, 17/28.33, "Defence Clips", 0)

        # pdf.image(input_dict['backfoot_defense_qr'], 736.16/28.33, 250/28.33, 70.26/28.33, 70.95/28.33)

        # pdf.set_text_color(0,0,0)
        # pdf.set_font("ppneuemontreal", "BI", 12)
        # pdf.set_y(510/28.33)
        # pdf.set_x(575/28.33)
        # pdf.cell(743.61/28.33, 221.95/28.33, "Scan to view the video", 0)

    if input_dict['power_hitting']:
        ##Seventh Page-----------------------------------------------------------------------------------------------------------------------

        pdf.add_page()

        pdf.set_fill_color(8,11,119)
        pdf.rect(0, 0, pdf.w, 3, 'F')

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "", 34)
        pdf.set_y(18/28.33)
        pdf.set_x(33.88/28.33)
        pdf.cell(270/28.33, 52/28.33, "Power hitting drill", 0)

        pdf.set_fill_color(255,255,255)
        pdf.rect(300/28.33, 18/28.33, 51.78/28.33, 51.78/28.33, "F",round_corners=True)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "BI", 29.59)
        pdf.set_y(27/28.33)
        pdf.set_x(308/28.33)
        pdf.cell(36/28.33, 36/28.33, input_dict['power_hitting_rating'], 0)

        pdf.image(KPro_Logo_white, 661/28.33, 18/28.33)

        pdf.image(input_dict['power_hitting_qr'], 763/28.33, 18/28.33, 44/28.33, 44/28.33)

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "BI", 6)
        pdf.set_y(65/28.33)
        pdf.set_x(753/28.33)
        pdf.cell(53/28.33, 7/28.33, "Scan to view the video", 0)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 14)
        pdf.set_y(95/28.33)
        pdf.set_x(34/28.33)
        pdf.cell(85/28.33, 17/28.33, "Power hitting", 0)

        pdf.image(input_dict['power_hitting_1'], 40.75/28.33, 123.35/28.33, 380.25/28.33, 213.81/28.33)

        pdf.image(input_dict['power_hitting_2'], 40.75/28.33, 344.28/28.33, 380.25/28.33, 213.81/28.33)

        # pdf.set_text_color(0,0,0)
        # pdf.set_font("ppneuemontreal", "BI", 12)
        # pdf.set_y(108.47/28.33)
        # pdf.set_x(455.84/28.33)
        # pdf.cell(22/28.33, 14/28.33, "Grip", 0)

        # pdf.image("page7_image3.jpg", 457.23/28.33, 131.48/28.33, 69.96/28.33, 55.62/28.33)

        # pdf.image("page7_image4.jpg", 537.15/28.33, 131.48/28.33, 72.11/28.33, 55.52/28.33)

        # pdf.image("page7_image5.jpg", 614.76/28.33, 131.48/28.33, 89.03/28.33, 55.52/28.33)

        # pdf.image("page7_image6.jpg", 709.28/28.33, 131.48/28.33, 73.37/28.33, 55.52/28.33)

        white = (255, 255, 255)
        black = (0,0,0)
        headings_style = FontFace(color=white, fill_color=black)

        # TABLE_DATA = (
        #     ("Balls", "Launch angle", "Ball speed before", "Ball speed after", "Bat speed"),
        #     ("Ball 1", "30°", "130 Kmph", "140 Kmph", "70 Kmph"),
        #     ("Ball 2", "34°", "130 Kmph", "140 Kmph", "70 Kmph"),
        #     ("Ball 3", "40°", "130 Kmph", "140 Kmph", "70 Kmph"),
        #     ("Ball 4", "45°", "130 Kmph", "140 Kmph", "70 Kmph"),
        #     ("Ball 5", "45°", "130 Kmph", "140 Kmph", "70 Kmph"),
        #     ("Ball 6", "45°", "130 Kmph", "140 Kmph", "70 Kmph"),  
        # )

        TABLE_DATA = input_dict['power_hitting_table']

        pdf.set_y(108.47/28.33)
        pdf.set_x(455.84/28.33)
        pdf.set_fill_color(255,255,255)
        pdf.set_draw_color(0,0,0)
        pdf.set_font("ppneuemontreal","BI",8,)
        pdf.set_line_width(0.02)

        with pdf.table(
            headings_style=headings_style,
            width=12,
            col_widths=(3, 3, 3, 3, 3),
            text_align="CENTER",
            align="LEFT",
        ) as table:
            for data_row in TABLE_DATA:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "B", 14)
        # pdf.set_y(356.47/28.33)
        # pdf.set_x(458.9/28.33)
        # pdf.cell(45/28.33, 14/28.33, f"Insights: {input_dict['power_hitting_insights']}", 0)

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "BI", 8)
        # pdf.set_y(356.47/28.33)
        # pdf.set_x(458.9/28.33)
        # pdf.multi_cell(325.44/28.33, 64/28.33, "                    Keeping the head still and level is crucial for maintaining focus and judgement of the ball. A steady head allows batsmen to track the ball more accurately, making it easier to select and execute shots effectively.")            

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "B", 14)
        pdf.set_y(250/28.33)
        pdf.set_x(455/28.33)
        pdf.cell(45/28.33, 14/28.33, "Insights:", 0)

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "BI", 11)
        pdf.set_y(270/28.33)
        pdf.set_x(455/28.33)
        pdf.multi_cell(263.9/28.33, 14/28.33, f"{input_dict['power_hitting_insights']}")

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "B", 14)
        # pdf.set_y(380/28.33)
        # pdf.set_x(455/28.33)
        # pdf.cell(45/28.33, 14/28.33, "Improvements:", 0)


        pdf.set_fill_color(255, 204, 21)
        pdf.rect(435/28.33, 430.64/28.33, 410/28.33, 179.36/28.33, 'F') # modified

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "B", 14)
        pdf.set_y(450/28.33)
        pdf.set_x(455/28.33)
        pdf.cell(45/28.33, 14/28.33, "Improvements:", 0)

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "BI", 11)
        pdf.set_y(470/28.33)
        pdf.set_x(455/28.33)
        pdf.multi_cell(300/28.33, 12/28.33, f"{input_dict['power_hitting_improvements']}", 0,max_line_height=0.5,align='L')

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "BI", 13)
        # pdf.set_y(380/28.33)
        # pdf.set_x(455/28.33)
        # pdf.multi_cell(263.9/28.33, 14/28.33, f"                                            {input_dict['power_hitting_improvements']}")


        # pdf.image(input_dict['power_hitting_qr'], 456.88/28.33, 480.15/28.33, 60.26/28.33, 60.95/28.33)

        

        # pdf.set_text_color(0,0,0)
        # pdf.set_font("ppneuemontreal", "BI", 12)
        # pdf.set_y(530.09/28.33)
        # pdf.set_x(464.33/28.33)
        # pdf.cell(82.37/28.33, 28/28.33, "Scan to view the video", 0)

    if input_dict['running_bw']:
        ##Eighth Page-----------------------------------------------------------------------------------------------------------------------

        pdf.add_page()

        pdf.set_fill_color(8,11,119)
        pdf.rect(0, 0, pdf.w, 3, 'F')

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "", 34)
        pdf.set_y(18/28.33)
        pdf.set_x(33.88/28.33)
        pdf.cell(305/28.33, 52/28.33, "Running b/w wickets", 0)

        pdf.set_fill_color(255,255,255)
        pdf.rect(355/28.33, 18/28.33, 51.78/28.33, 51.78/28.33, "F",round_corners=True)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "BI", 29.59)
        pdf.set_y(27/28.33)
        pdf.set_x(363/28.33)
        pdf.cell(36/28.33, 36/28.33, input_dict['running_bw_rating'], 0)

        pdf.image(KPro_Logo_white, 661/28.33, 18/28.33)

        pdf.image(input_dict['running_bw_qr'], 763/28.33, 18/28.33, 44/28.33, 44/28.33)

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "BI", 6)
        pdf.set_y(65/28.33)
        pdf.set_x(753/28.33)
        pdf.cell(53/28.33, 7/28.33, "Scan to view the video", 0)

        pdf.set_text_color(114,114,114)
        pdf.set_font("ppneuemontreal", "", 14)
        pdf.set_y(95/28.33)
        pdf.set_x(34/28.33)
        pdf.cell(157/28.33, 17/28.33, "Running b/w wickets set 1", 0)

        #-----------------------------------------------------------------------------------------

        # pdf.set_text_color(0,0,0)
        # pdf.set_font("ppneuemontreal", "", 14)
        # pdf.set_y(130/28.33)
        # pdf.set_x(34/28.33)
        # pdf.cell(70/28.33, 17/28.33, "Run a three", 0)

        # pdf.set_text_color(241,1,1)
        # pdf.set_font("ppneuemontreal", "", 14)
        # pdf.set_y(130/28.33)
        # pdf.set_x(109/28.33)
        # pdf.cell(52/28.33, 17/28.33, "7:56 secs", 0)

        pdf.image(input_dict['running_bw_1'], 34/28.33, 152/28.33, 212.53/28.33, 424.1/28.33)

        #------------------------------------------------------------------------------------------

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 14)
        pdf.set_y(130/28.33)
        pdf.set_x(264.53/28.33)
        pdf.cell(64/28.33, 17/28.33, "Run a 3:", 0)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 14)
        pdf.set_y(130/28.33)
        pdf.set_x(333.53/28.33)
        pdf.cell(52/28.33, 17/28.33, f"{input_dict['run_time']} secs", 0)

        pdf.image(input_dict['running_bw_2'], 264.53/28.33, 152/28.33, 212.53/28.33, 424.1/28.33)

        pdf.set_text_color(114,114,114)
        pdf.set_font("ppneuemontreal", "", 14)
        pdf.set_y(100/28.33)
        pdf.set_x(514.91/28.33)
        pdf.cell(126/28.33, 17/28.33, "Running b/w wickets", 0)

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "B", 14)
        pdf.set_y(138.7/28.33)
        pdf.set_x(518.62/28.33)
        pdf.cell(45/28.33, 14/28.33, "Insights:", 0)

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "BI", 11)
        pdf.set_y(158.7/28.33)
        pdf.set_x(518.62/28.33)
        pdf.multi_cell(263.9/28.33, 14/28.33, f"{input_dict['running_bw_insights']}")


        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "", 14)
        pdf.set_y(290/28.33)
        pdf.set_x(518.62/28.33)
        pdf.cell(45/28.33, 14/28.33, "Avg Timing Benchmark:", 0)

        pdf.set_fill_color(255, 204, 21)
        pdf.rect(476.8/28.33, 440.64/28.33, 365.2/28.33, 179.36/28.33, 'F') # modified

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "B", 14)
        pdf.set_y(450/28.33)
        pdf.set_x(518.62/28.33)
        pdf.cell(45/28.33, 14/28.33, "Improvements:", 0)

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "BI", 11)
        pdf.set_y(470/28.33)
        pdf.set_x(518.62/28.33)
        pdf.multi_cell(300/28.33, 12/28.33, f"{input_dict['running_bw_improvements']}", 0,max_line_height=0.5,align='L')

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "B", 14)
        # pdf.set_y(250/28.33)
        # pdf.set_x(518.62/28.33)
        # pdf.cell(45/28.33, 14/28.33, "Improvements:", 0)

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "BI", 13)
        # pdf.set_y(250/28.33)
        # pdf.set_x(518.62/28.33)
        # pdf.multi_cell(263.9/28.33, 14/28.33, f"                                    {input_dict['running_bw_improvements']}")

        # pdf.image("page8_image3.jpg", 514.91/28.33, 294.55/28.33, 205.7/28.33, 139/28.33)

        # Bar chart section
        # Chart properties
        chart_x = 518 / 28.33  # X-coordinate of the chart's starting point
        chart_y = 350 / 28.33  # Y-coordinate of the chart's starting point
        bar_width = 50 / 28.33  # Width of each bar
        max_height = 50 / 28.33  # Height of the tallest bar (relative to the largest value)
        bar_spacing = 20 / 28.33  # Spacing between bars

        # Data for the bars
        avg_time = input_dict['avg_time']  # Average time (units)
        actual_time = input_dict['run_time']  # Actual time (units)
        max_units = max(avg_time, actual_time)  # Maximum units for scaling

        # Draw the horizontal dotted axes and vertical axis labels
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("ppneuemontreal", "", 10)
        num_labels = 5  # Number of labels (e.g., 3, 6, 9, ...)
        for i in range(1, num_labels + 1):
            label_value = i * 3
            label_y = chart_y + max_height - (label_value / max_units * max_height)
            # Draw horizontal dotted line
            pdf.set_draw_color(150, 150, 150)
            # pdf.dashed_line(chart_x, label_y, chart_x + 150 / 28.33, label_y, 1, 1)  # Dotted line
            # Add label on the right
            pdf.set_y(label_y - 2 / 28.33)  # Adjust for vertical alignment
            pdf.set_x(chart_x + 130 / 28.33)  # Position labels to the right of the chart
            pdf.cell(10 / 28.33, 5 / 28.33, str(label_value), 0, 0, 'L')

        # Draw the bars
        # Bar 1: Average Time
        pdf.set_fill_color(100, 149, 237)  # Blue color for the average time
        bar1_height = avg_time / max_units * max_height
        pdf.rect(chart_x, chart_y + max_height - bar1_height, bar_width, bar1_height, 'F')

        # Add average time inside the bar
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("ppneuemontreal", "", 10)
        pdf.set_y(chart_y + max_height - bar1_height / 2 - 2 / 28.33)
        pdf.set_x(chart_x + bar_width / 2 - 5 / 28.33)
        pdf.cell(10 / 28.33, 5 / 28.33, str(avg_time), 0, 0, 'C')

        # Bar 2: Actual Time
        pdf.set_fill_color(255, 99, 71)  # Red color for the actual time
        bar2_height = actual_time / max_units * max_height
        pdf.rect(chart_x + bar_width + bar_spacing, chart_y + max_height - bar2_height, bar_width, bar2_height, 'F')

        # Add actual time inside the bar
        pdf.set_y(chart_y + max_height - bar2_height / 2 - 2 / 28.33)
        pdf.set_x(chart_x + bar_width + bar_spacing + bar_width / 2 - 5 / 28.33)
        pdf.cell(10 / 28.33, 5 / 28.33, str(actual_time), 0, 0, 'C')

        # Add labels for the bars
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("ppneuemontreal", "", 12)

        # Label for Bar 1
        pdf.set_y(chart_y + max_height + 5 / 28.33)  # Slightly below the chart
        pdf.set_x(chart_x)
        pdf.cell(bar_width, 5 / 28.33, "Avg Time", 0, 0, 'C')

        # Label for Bar 2
        pdf.set_x(chart_x + bar_width + bar_spacing)
        pdf.cell(bar_width, 5 / 28.33, "Actual Time", 0, 0, 'C')


        # pdf.image(input_dict['running_bw_qr'], 734.01/28.33, 446.89/28.33, 97.26/28.33, 124.95/28.33)


    if input_dict['point_of_contact']:
        ##Ninth Page-----------------------------------------------------------------------------------------------------------------------
    
        pdf.add_page()

        pdf.set_fill_color(8,11,119)
        pdf.rect(0, 0, pdf.w, 2.39, 'F')

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "", 34)
        pdf.set_y(7.89/28.33)
        pdf.set_x(33.88/28.33)
        pdf.cell(237/28.33, 52/28.33, "Point of contact", 0)

        pdf.set_fill_color(255,255,255)
        pdf.rect(277.88/28.33, 7.89/28.33, 51.78/28.33, 51.78/28.33, "F",round_corners=True)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "BI", 29.59)
        pdf.set_y(17/28.33)
        pdf.set_x(285.77/28.33)
        pdf.cell(36/28.33, 36/28.33, input_dict['point_of_contact_rating'], 0)

        pdf.image("qr_code", 757.17/28.33, 8.5/28.33, 50.95/28.33, 50.79/28.33)
        #-------------------------------------------------------------------------------------------------
        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 10)
        pdf.set_y(103.81/28.33)
        pdf.set_x(34/28.33)
        pdf.cell(62/28.33, 13/28.33, "Ball 1 - Perfect", 0)

        pdf.image("page9_image1.jpg", 33.88/28.33, 122.01/28.33, 286.75/28.33, 122.41/28.33)

        #-------------------------------------------------------------------------------------------------

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 10)
        pdf.set_y(103.81/28.33)
        pdf.set_x(336.62/28.33)
        pdf.cell(62/28.33, 13/28.33, "Ball 2 - Good", 0)

        pdf.image("page9_image1.jpg", 336.62/28.33, 122.01/28.33, 286.75/28.33, 122.41/28.33)

        #-------------------------------------------------------------------------------------------------

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 10)
        pdf.set_y(262.5/28.33)
        pdf.set_x(34/28.33)
        pdf.cell(62/28.33, 13/28.33, "Ball 3 - Poor", 0)

        pdf.image("page9_image1.jpg", 33.38/28.33, 280.42/28.33, 286.75/28.33, 122.41/28.33)

        #-------------------------------------------------------------------------------------------------

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 10)
        pdf.set_y(262.5/28.33)
        pdf.set_x(336.62/28.33)
        pdf.cell(62/28.33, 13/28.33, "Ball 4 - Perfect", 0)

        pdf.image("page9_image1.jpg", 336.62/28.33, 280.42/28.33, 286.75/28.33, 122.41/28.33)

        #-------------------------------------------------------------------------------------------------

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 10)
        pdf.set_y(421.19/28.33)
        pdf.set_x(34/28.33)
        pdf.cell(62/28.33, 13/28.33, "Ball 5 - Good", 0)

        pdf.image("page9_image1.jpg", 33.38/28.33, 438.84/28.33, 286.75/28.33, 122.41/28.33)

        #-------------------------------------------------------------------------------------------------

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "", 10)
        pdf.set_y(421.19/28.33)
        pdf.set_x(336.62/28.33)
        pdf.cell(62/28.33, 13/28.33, "Ball 6 - Perfect", 0)

        pdf.image("page9_image1.jpg", 336.62/28.33, 438.84/28.33, 286.75/28.33, 122.41/28.33)

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "B", 14)
        pdf.set_y(130.19/28.33)
        pdf.set_x(640.58/28.33)
        pdf.cell(45/28.33, 14/28.33, "Insights 1:", 0)

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "BI", 13)
        # pdf.set_y(130.19/28.33)
        # pdf.set_x(640.58/28.33)
        # pdf.multi_cell(192.43/28.33, 48/28.33, "Each image has a  metric of shot type & hold time.")

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "BI", 13)
        pdf.set_y(130.19/28.33)
        pdf.set_x(640.58/28.33)
        pdf.multi_cell(192.43/28.33, 64/28.33, "<perfect is under the chin, good is little away and poor is far>.")

        pdf.image("qr_code_text", 692/28.33, 436.81/28.33, 97.26/28.33, 124.95/28.33)

    if input_dict['hold_your_pose']:
        ##Tenth Page-----------------------------------------------------------------------------------------------------------------------

        pdf.add_page()

        pdf.set_fill_color(8,11,119)
        pdf.rect(0, 0, pdf.w, 3, 'F')

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "", 34)
        pdf.set_y(18/28.33)
        pdf.set_x(33.88/28.33)
        pdf.cell(237/28.33, 52/28.33, "Hold your pose", 0)

        pdf.set_fill_color(255,255,255)
        pdf.rect(277.88/28.33, 18/28.33, 51.78/28.33, 51.78/28.33, "F",round_corners=True)

        pdf.set_text_color(0,0,0)
        pdf.set_font("ppneuemontreal", "BI", 29.59)
        pdf.set_y(27/28.33)
        pdf.set_x(285.77/28.33)
        pdf.cell(36/28.33, 36/28.33, input_dict['hold_your_pose_rating'], 0)

        pdf.image(KPro_Logo_white, 661/28.33, 18/28.33)

        pdf.image(input_dict['hold_your_pose_qr'], 763/28.33, 18/28.33, 44/28.33, 44/28.33)

        pdf.set_text_color(255,255,255)
        pdf.set_font("ppneuemontreal", "BI", 6)
        pdf.set_y(65/28.33)
        pdf.set_x(753/28.33)
        pdf.cell(53/28.33, 7/28.33, "Scan to view the video", 0)
        #-------------------------------------------------------------------------------------------------

        if input_dict['hold_your_pose_1']:
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "", 10)
            pdf.set_y(103.81/28.33)
            pdf.set_x(34/28.33)
            pdf.cell(62/28.33, 13/28.33, f"Ball 1", 0)

            # pdf.image(input_dict['hold_your_pose_1'], 33.88/28.33, 122.01/28.33, 286.75/28.33, 122.41/28.33)
            pdf.image(input_dict['hold_your_pose_1'], 33.88/28.33, 122.01/28.33, 130/28.33, 200/28.33)

        #-------------------------------------------------------------------------------------------------

        if input_dict['hold_your_pose_2']:
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "", 10)
            pdf.set_y(103.81/28.33)
            # pdf.set_x(336.62/28.33)
            pdf.set_x(190/28.33)
            pdf.cell(62/28.33, 13/28.33, f"Ball 2", 0)

            # pdf.image(input_dict['hold_your_pose_2'], 336.62/28.33, 122.01/28.33, 286.75/28.33, 122.41/28.33)
            pdf.image(input_dict['hold_your_pose_2'], 190/28.33, 122.01/28.33, 130/28.33, 200/28.33)

        #-------------------------------------------------------------------------------------------------

        if input_dict['hold_your_pose_3']:
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "", 10)
            # pdf.set_y(262.5/28.33)
            pdf.set_y(103.81/28.33)
            # pdf.set_x(34/28.33)
            pdf.set_x(340/28.33)
            pdf.cell(62/28.33, 13/28.33, f"Ball 3", 0)

            # pdf.image(input_dict['hold_your_pose_3'], 33.38/28.33, 280.42/28.33, 286.75/28.33, 122.41/28.33)
            pdf.image(input_dict['hold_your_pose_3'], 340/28.33, 122.01/28.33, 130/28.33, 200/28.33)

        #-------------------------------------------------------------------------------------------------

        if input_dict['hold_your_pose_4']:
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "", 10)
            # pdf.set_y(262.5/28.33)
            pdf.set_y(330/28.33)
            # pdf.set_x(336.62/28.33)
            pdf.set_x(34/28.33)
            pdf.cell(62/28.33, 13/28.33, f"Ball 4", 0)

            # pdf.image(input_dict['hold_your_pose_4'], 336.62/28.33, 280.42/28.33, 286.75/28.33, 122.41/28.33)
            pdf.image(input_dict['hold_your_pose_4'], 33.88/28.33, 350/28.33, 130/28.33, 200/28.33)

        #-------------------------------------------------------------------------------------------------

        if input_dict['hold_your_pose_5']:
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "", 10)
            # pdf.set_y(421.19/28.33)
            pdf.set_y(330/28.33)
            # pdf.set_x(34/28.33)
            pdf.set_x(190/28.33)
            pdf.cell(62/28.33, 13/28.33, f"Ball 5", 0)

            # pdf.image(input_dict['hold_your_pose_5'], 33.38/28.33, 438.84/28.33, 286.75/28.33, 122.41/28.33)
            pdf.image(input_dict['hold_your_pose_5'], 190/28.33, 350/28.33, 130/28.33, 200/28.33)

        #-------------------------------------------------------------------------------------------------

        if input_dict['hold_your_pose_6']:
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "", 10)
            # pdf.set_y(421.19/28.33)
            pdf.set_y(330/28.33)
            # pdf.set_x(336.62/28.33)
            pdf.set_x(340/28.33)
            pdf.cell(62/28.33, 13/28.33, f"Ball 6", 0)

            # pdf.image(input_dict['hold_your_pose_6'], 336.62/28.33, 438.84/28.33, 286.75/28.33, 122.41/28.33)
            pdf.image(input_dict['hold_your_pose_6'], 340/28.33, 350/28.33, 130/28.33, 200/28.33)

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "B", 14)
        # pdf.set_y(130.19/28.33)
        # pdf.set_x(500/28.33)
        # pdf.cell(45/28.33, 14/28.33, "Insights 1", 0)

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "BI", 13)
        # pdf.set_y(130.19/28.33)
        # pdf.set_x(500/28.33)
        # pdf.multi_cell(192.43/28.33, 48/28.33, input_dict['hold_your_pose_insights'])


        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "B", 14)
        pdf.set_y(111/28.33)
        pdf.set_x(518.62/28.33)
        pdf.cell(45/28.33, 14/28.33, "Insights:", 0)

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "BI", 13)
        # pdf.set_y(128.7/28.33)
        # pdf.set_x(518.62/28.33)
        # pdf.multi_cell(280/28.33, 14/28.33, f"                      {input_dict['tophand_insights']}", 0,max_line_height=0.5,align='L')
        
        box_y = 130

        if input_dict['hold_your_pose_1_duration']:
            pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
            pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(570/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, f"{input_dict['hold_your_pose_1_duration']} Sec",0)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, "Ball 1",0) 

            pdf.set_y((box_y+2+18)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(272/28.33, 27/28.33, input_dict['hold_your_pose_1_comment'], 0)

        box_y += 50

        if input_dict['hold_your_pose_2_duration']:
            pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
            pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(570/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, f"{input_dict['hold_your_pose_2_duration']} Sec",0)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, "Ball 2",0) 

            # Ball Review Comment
            pdf.set_y((box_y+2+18)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(272/28.33, 27/28.33, input_dict['hold_your_pose_2_comment'], 0)

        box_y += 50

        if input_dict['hold_your_pose_3_duration']:
            pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
            pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(570/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, f"{input_dict['hold_your_pose_3_duration']} Sec",0)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, "Ball 3",0) 

            # Ball Review Comment
            pdf.set_y((box_y+2+18)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(272/28.33, 27/28.33, input_dict['hold_your_pose_3_comment'], 0)

        box_y += 50

        if input_dict['hold_your_pose_4_duration']:
            pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
            pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(570/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, f"{input_dict['hold_your_pose_4_duration']} Sec",0)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, "Ball 4",0) 

            # Ball Review Comment
            pdf.set_y((box_y+2+18)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(272/28.33, 27/28.33, input_dict['hold_your_pose_4_comment'], 0)

        box_y += 50

        if input_dict['hold_your_pose_5_duration']:
            pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
            pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(570/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, f"{input_dict['hold_your_pose_5_duration']} Sec",0)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, "Ball 5",0) 

            # Ball Review Comment
            pdf.set_y((box_y+2+18)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(272/28.33, 27/28.33, input_dict['hold_your_pose_5_comment'], 0)

        box_y += 50

        if input_dict['hold_your_pose_6_duration']:
            pdf.rect(518/28.33, box_y/28.33, 44/28.33, 22/28.33)
            pdf.rect(562/28.33, box_y/28.33, 76/28.33, 22/28.33)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(570/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, f"{input_dict['hold_your_pose_6_duration']} Sec",0)
            pdf.set_text_color(0,0,0)
            pdf.set_font("ppneuemontreal", "",  12)
            pdf.set_y((box_y+2)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(24/28.33, 16/28.33, "Ball 6",0) 

            # Ball Review Comment
            pdf.set_y((box_y+2+18)/28.33)
            pdf.set_x(524/28.33)#+6
            pdf.cell(272/28.33, 27/28.33, input_dict['hold_your_pose_6_comment'], 0)
        

        pdf.set_fill_color(255, 204, 21)
        pdf.rect(476.8/28.33, 440.64/28.33, 365.2/28.33, 179.36/28.33, 'F') # modified

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "B", 14)
        pdf.set_y(450/28.33)
        pdf.set_x(518.62/28.33)
        pdf.cell(45/28.33, 14/28.33, "Improvements:", 0)

        pdf.set_text_color(2,2,2)
        pdf.set_font("ppneuemontreal", "BI", 11)
        pdf.set_y(470/28.33)
        pdf.set_x(518.62/28.33)
        pdf.multi_cell(300/28.33, 12/28.33, f"{input_dict['hold_your_pose_improvements']}", 0,max_line_height=0.5,align='L')


        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "B", 14)
        # pdf.set_y(128.7/28.33)
        # pdf.set_x(518.62/28.33)
        # pdf.cell(45/28.33, 14/28.33, "Insights:", 0)

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "BI", 13)
        # pdf.set_y(128.7/28.33)
        # pdf.set_x(518.62/28.33)
        # pdf.multi_cell(263.9/28.33, 14/28.33, f"                    {input_dict['hold_your_pose_insights']}") 

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "B", 14)
        # pdf.set_y(240/28.33)
        # pdf.set_x(518.62/28.33)
        # pdf.cell(45/28.33, 14/28.33, "Improvements:", 0)

        # pdf.set_text_color(2,2,2)
        # pdf.set_font("ppneuemontreal", "BI", 13)
        # pdf.set_y(240/28.33)
        # pdf.set_x(518.62/28.33)
        # pdf.multi_cell(263.9/28.33, 14/28.33, f"                                        {input_dict['hold_your_pose_improvements']}")



        # pdf.image(input_dict['hold_your_pose_qr'], 692/28.33, 436.81/28.33, 97.26/28.33, 124.95/28.33)


    ## Second Last Page ## 

    # Second last page Image
    second_last_page_image = "content/page_2nd_last.jpg"

    pdf.add_page()

    pdf.image(second_last_page_image, 0, 0, 841.89/28.33, 595.28/28.33)

    ## Last Page ##
    # Last page Image
    last_page_image = "content/page_last.jpg"
    # last_page_image = 'last_page_new.png'

    pdf.add_page()

    pdf.image(last_page_image, 0, 0, 841.89/28.33, 595.28/28.33)

    final_filename = input_dict['player_name'] + "_batting_assessment.pdf"
    pdf.output(final_filename)
    return final_filename


def generate_power_hitting_table(data):
    power_hitting = data["drill_metrics"]["power_hitting"]
    metrics = power_hitting["ball_metrics"]
    
    table = [
        ("Balls", "Launch angle", "Ball speed before", "Ball speed after", "Bat speed")
    ]
    
    for i in range(6):  # For Ball 1 to Ball 6
        row = (
            f"Ball {i+1}",
            f"{metrics['launch_angles'][i]}°",
            f"{metrics['ball_speeds_before'][i]} Kmph",
            f"{metrics['ball_speeds_after'][i]} Kmph",
            f"{metrics['bat_speeds'][i]} Kmph"
        )
        table.append(row)
    
    return tuple(table)

def google_drive_url_to_image(url, output_path):
    """Handles Google Drive URLs specifically"""
    try:
        # Extract Google Drive file ID
        file_id = None
        if 'drive.google.com' in url:
            match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
            if match:
                file_id = match.group(1)
            else:  # Handle URL parameters format
                params = parse_qs(urlparse(url).query)
                file_id = params.get('id', [None])[0]
        
        if not file_id:
            raise ValueError("Invalid Google Drive URL")

        # Construct direct download URL
        direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        # Start download session
        session = requests.Session()
        response = session.get(direct_url, stream=True)

        # Handle large file confirmation
        if "confirm=" in response.url:
            # Extract confirmation token
            confirm_token = re.findall(r'confirm=([a-zA-Z0-9_-]+)', response.url)[0]
            direct_url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm_token}"
            response = session.get(direct_url, stream=True)

        # Detect content type
        content_type = response.headers.get('Content-Type', '')
        # ... (use the content-type detection logic from previous version) ...

        # Save file (using previous version's saving logic)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)

        print(f"Successfully downloaded from Google Drive: {output_path}")
        return output_path

    except Exception as e:
        print(f"Google Drive download failed: {str(e)}")
        return None

def get_ai_feedback(skill_map_values):
    # Import the required libraries
    api_key = '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'
    client = Groq(api_key=api_key)

    few_shot_examples = [

        "The player's skill map shows a strong bottom-hand grip, but top-hand control and running skills need further development. Drills for power, balance, backfoot technique, and feet planting have not been conducted. Incorporating these drills will address weaknesses and contribute to a more well-rounded skill set, enhancing overall performance."
        "The player's skill map shows strong bottom-hand grip and excellent top-hand control. However, drills for power, running, balance, backfoot technique, and feet planting have not been conducted. Incorporating these drills will help further enhance skills and ensure more comprehensive development"
    ]   



    prompt = f""" 
    Generate one Paragraph for Skill Map Feedback, based on Below Data:

    Skill Map Values Include the Following:
    1. Power: {skill_map_values['power']}
    2. Balance: {skill_map_values['balance']}
    3. Bottomhand Grip: {skill_map_values['grip']}
    4. Running: {skill_map_values['running']}
    5. Backfoot Technique: {skill_map_values['poc']}
    6. Feet Planted: {skill_map_values['feet_planted']}
    7. Top Hand Control: {skill_map_values['control']}

    Percentile values are from 1-100. Value 0 means drill is not conducted. First Comment on Drills which are conducted, then When drill is not conducted, mention it and suggest to conduct the drill.
    
    Consider Format from Few Shot Examples: {few_shot_examples}

    Generate Skill Map Feedback in Text Format With Strictly Not More than 300 Characters and 50 Words (No Preamble):
 
    """

    chat_completion = client.chat.completions.create(
        #
        # Required parameters
        #
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": "you are an Expert Cricket Coach"
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": prompt,
            }
        ],

        # The language model which will generate the completion.
        model='deepseek-r1-distill-llama-70b',

        temperature=0.5,

        # max_completion_tokens=200,

        top_p=1,

        stop=None,

        # If set, partial message deltas will be sent.
        stream=False,
    )

    

    return chat_completion.choices[0].message.content

def generate_report(assessment_id):
    uri = "mongodb+srv://aman:N3cLLYBTrKMTElAS@kpro-staging.f3esdpg.mongodb.net/"

    drills_crud = BattingDrillsCRUD(uri)

    document = drills_crud.get_document(assessment_id)

    skill_map_values = {
        # SKILL MAP VALUES # 
        'power': document['drill_metrics'].get('power_hitting', {}).get('percentile', 0), # Power Hitting
        'grip': document['drill_metrics'].get('bottom_hand', {}).get('percentile', 0), # Bottom Hand Grip
        'control': document['drill_metrics'].get('top_hand', {}).get('percentile', 0), # Top Hand
        'running': document['drill_metrics'].get('running_bw_wickets', {}).get('percentile', 0), # Running Between Wickets
        'balance': document['drill_metrics'].get('hold_your_pose', {}).get('percentile', 0), # Hold Your Pose
        'poc': document['drill_metrics'].get('backfoot', {}).get('percentile', 0), # Point of Contact
        'feet_planted': document['drill_metrics'].get('feet_planted', {}).get('percentile', 0), # Feet Planted
    }

    while True:
        try:
            feedback = get_ai_feedback(skill_map_values)
            skill_map_feedback = feedback.split('</think>')[-1].strip()
            break
            # print(feedback)
        except:
            continue


    # Shivi
    # TABLE_DATA = (
    #     ("Balls", "Launch angle", "Ball speed before", "Ball speed after", "Bat speed"),
    #     ("Ball 1", "17.35°", "34.25 Kmph", "66.05 Kmph", "52.31 Kmph"),
    #     ("Ball 2", "28.54°", "25.21 Kmph", "51.14 Kmph", "89.97 Kmph"),
    #     ("Ball 3", "26.71°", "17.67 Kmph", "52.88 Kmph", "53.14 Kmph"),
    #     ("Ball 4", "10.98°", "24.98 Kmph", "56.98 Kmph", "58.32 Kmph"),
    #     ("Ball 5", "25.76°", "24.59 Kmph", "46.48 Kmph", "50.62 Kmph"),
    #     ("Ball 6", "10.61°", "19.14 Kmph", "54.28 Kmph", "64.03 Kmph"),
    # )


    # Drills Conducted
    tophand_flag = document['drill_metrics'].get('top_hand', {}).get('drill_conducted', False)
    bottomhand_flag = document['drill_metrics'].get('bottom_hand', {}).get('drill_conducted', False)
    backfootdrive_flag = document['drill_metrics'].get('backfoot', {}).get('drill_conducted', False)
    backfootdefense_flag = document['drill_metrics'].get('backfoot', {}).get('drill_conducted', False)
    power_hitting_flag = document['drill_metrics'].get('power_hitting', {}).get('drill_conducted', False)
    running_bw_flag = document['drill_metrics'].get('running_bw_wickets', {}).get('drill_conducted', False)
    point_of_contact_flag = False
    hold_your_pose_flag = document['drill_metrics'].get('hold_your_pose', {}).get('drill_conducted', False)
    feetplanted_flag = document['drill_metrics'].get('feet_planted', {}).get('drill_conducted', False)

    if power_hitting_flag:
        power_hitting_table = generate_power_hitting_table(document)
        table_data = power_hitting_table

    if tophand_flag:

        tophand_ball_insights = document['drill_metrics']['top_hand']['insights']['ball_insights']
        tophand_ball_comments =  document['drill_metrics']['top_hand']['insights']['ball_comments']

    if bottomhand_flag:

        bottomhand_ball_insights = document['drill_metrics']['bottom_hand']['insights']['ball_insights']
        bottomhand_ball_comments = document['drill_metrics']['bottom_hand']['insights']['ball_comments']

    if hold_your_pose_flag:

        hold_your_pose_ball_durations = document['drill_metrics']['hold_your_pose']['insights']['ball_durations']
        hold_your_pose_ball_comments = document['drill_metrics']['hold_your_pose']['insights']['ball_comments']
    # feet_planted_ball_insights = document['drill_metrics']['feet_planted']['insights']['ball_insights']
    # feet_planted_ball_comments = document['drill_metrics']['feet_planted']['insights']['ball_comments']
    batter_name = document['player_details']['player_name']



    input_dict = { 


        'skill_map_feedback': skill_map_feedback,

        # DRILLS CONDUCTED
        'tophand': tophand_flag,
        'bottomhand': bottomhand_flag,
        'backfootdrive': backfootdrive_flag,
        'backfootdefense': backfootdefense_flag,
        'power_hitting': power_hitting_flag,
        'running_bw': running_bw_flag,
        'point_of_contact': point_of_contact_flag,
        'hold_your_pose': hold_your_pose_flag,
        'feetplanted': feetplanted_flag,

        'tophand_qr': google_drive_url_to_image( document['drill_metrics']['top_hand']['drill_qr_path'],f"tophand_qr.jpg"), # Still include extension for safety,
        'bottomhand_qr': google_drive_url_to_image( document['drill_metrics']['bottom_hand']['drill_qr_path'],"bottomhand_qr.jpg"),
        'backfoot_drive_qr': google_drive_url_to_image( document['drill_metrics']['backfoot']['drill_qr_path'],"backfoot_drive_qr.jpg"),
        'backfoot_defense_qr': google_drive_url_to_image( document['drill_metrics']['backfoot']['drill_qr_path2'],"backfoot_defence.jpg"),
        'running_bw_qr': google_drive_url_to_image( document['drill_metrics']['running_bw_wickets']['drill_qr_path'],"running_bw_qr.jpg"),
        'feet_planted_qr': google_drive_url_to_image( document['drill_metrics']['feet_planted']['drill_qr_path'],"feet_planted_qr.jpg"),
        'hold_your_pose_qr': google_drive_url_to_image( document['drill_metrics']['hold_your_pose']['drill_qr_path'],"hold_your_pose_qr.jpg") if hold_your_pose_flag else None,
        'power_hitting_qr': google_drive_url_to_image( document['drill_metrics']['power_hitting']['drill_qr_path'],"power_hitting_qr.jpg"),


        # PLAYER DETAILS 
        'player_name': document['player_details']['player_name'],
        'player_age': document['player_details']['player_age'],
        'player_gender': document['player_details']['player_gender'],
        'academy_name': document['player_details']['academy_name'],
        "assessment_date": document['drill_date'],
        'month_of_assessment': "Mar 2025",
        'overall_rating': document['overall_rating'],
        'arm': document['player_details']['arm'],

        # SKILL MAP VALUES # 
        'power': document['drill_metrics'].get('power_hitting', {}).get('percentile', 0), # Power Hitting
        'grip': document['drill_metrics'].get('bottom_hand', {}).get('percentile', 0), # Bottom Hand Grip
        'control': document['drill_metrics'].get('top_hand', {}).get('percentile', 0), # Top Hand
        'running': document['drill_metrics'].get('running_bw_wickets', {}).get('percentile', 0), # Running Between Wickets
        'balance': document['drill_metrics'].get('hold_your_pose', {}).get('percentile', 0), # Hold Your Pose
        'poc': document['drill_metrics'].get('backfoot', {}).get('percentile', 0), # Point of Contact
        'feet_planted': document['drill_metrics'].get('feet_planted', {}).get('percentile', 0), # Feet Planted
        

        # TOPHAND #
        'tophand_main': google_drive_url_to_image( document['drill_metrics']['top_hand']['main_path'],"tophand_main.jpg"),
        'tophand_return_direction': google_drive_url_to_image( document['drill_metrics']['top_hand']['return_direction_path'],"tophand_return_dir.jpg"),
        'tophand_mistake': None,
        'tophand_percentile': document['drill_metrics']['top_hand']['percentile'],
        'tophand_rating': document['drill_metrics']['top_hand']['grade'],
        # 'tophand_insights': 'The batter showed inconsistent performance in this drill, particularly struggling with accuracy and shot placement. While balls 3 and 4 were accurately played to the cover region as per the delivery line, balls 1, 2, 5, and 6 lacked precision. Ball 1 and ball 6 were mistimed to point, and ball 2 lacked the necessary timing and direction to cover. This indicates a need for better control and decision-making in shot execution.',
        'tophand_improvements': document['drill_metrics']['top_hand']['improvements'],
        
        'tophand_ball_1': tophand_ball_insights[0],
        'tophand_ball_1_comment': tophand_ball_comments[0],
        'tophand_ball_2': tophand_ball_insights[1],
        'tophand_ball_2_comment': tophand_ball_comments[1],
        'tophand_ball_3': tophand_ball_insights[2],
        'tophand_ball_3_comment': tophand_ball_comments[2],
        'tophand_ball_4': tophand_ball_insights[3],
        'tophand_ball_4_comment': tophand_ball_comments[3],
        'tophand_ball_5': tophand_ball_insights[4],
        'tophand_ball_5_comment': tophand_ball_comments[4],
        'tophand_ball_6': tophand_ball_insights[5],
        'tophand_ball_6_comment': tophand_ball_comments[5],


        # BOTTOMHAND #
        'bottomhand_main': google_drive_url_to_image( document['drill_metrics']['bottom_hand']['main_path'],"bottomhand_main.jpg"),
        'bottomhand_return_direction': google_drive_url_to_image( document['drill_metrics']['bottom_hand']['return_direction_path'],"bottomhand_return_dir.jpg"),
        'bottomhand_mistake': None,
        'bottomhand_percentile': document['drill_metrics']['bottom_hand']['percentile'],
        'bottomhand_rating': document['drill_metrics']['bottom_hand']['grade'],
        # 'bottomhand_insights': 'The batter performed well in this bottom-hand drill, demonstrating accurate placement on the first four balls, particularly to the cover and mid-off regions. However, there were two lapses: ball 5 was slightly mistimed, reducing its effectiveness, and ball 6 was poorly directed to square leg, which was not appropriate for an off-stump delivery.',
        'bottomhand_improvements': document['drill_metrics']['bottom_hand']['improvements'],
        
        'bottomhand_ball_1': bottomhand_ball_insights[0],
        'bottomhand_ball_1_comment': bottomhand_ball_comments[0],
        'bottomhand_ball_2': bottomhand_ball_insights[1],
        'bottomhand_ball_2_comment': bottomhand_ball_comments[1],
        'bottomhand_ball_3': bottomhand_ball_insights[2],
        'bottomhand_ball_3_comment': bottomhand_ball_comments[2],
        'bottomhand_ball_4': bottomhand_ball_insights[3],
        'bottomhand_ball_4_comment': bottomhand_ball_comments[3],
        'bottomhand_ball_5': bottomhand_ball_insights[4],
        'bottomhand_ball_5_comment': bottomhand_ball_comments[4],
        'bottomhand_ball_6': bottomhand_ball_insights[5],
        'bottomhand_ball_6_comment': bottomhand_ball_comments[5],

        # BACKFOOT #
        'backfoot_main': google_drive_url_to_image( document['drill_metrics']['backfoot']['main_path'],"backfoot_main.jpg"),
        'backfoot_return_direction': google_drive_url_to_image( document['drill_metrics']['backfoot']['return_direction_path'],"backfoot_return_dir.jpg"),
        'backfoot_mistake': None,
        'backfoot_percentile': document['drill_metrics']['backfoot']['percentile'],
        'backfoot_rating': document['drill_metrics']['backfoot']['grade'],
        'backfoot_insights': document['drill_metrics']['backfoot']['insights'],
        'backfoot_improvements': document['drill_metrics']['backfoot']['improvements'],

        'backfoot_defense1': google_drive_url_to_image( document['drill_metrics']['backfoot']['img_1'],"backfoot_img1.jpg"),
        'backfoot_defense2': google_drive_url_to_image( document['drill_metrics']['backfoot']['img_2'],"backfoot_img2.jpg"),
        'backfoot_defense3': google_drive_url_to_image( document['drill_metrics']['backfoot']['img_3'],"backfoot_img3.jpg"),
        'backfoot_defense4': google_drive_url_to_image( document['drill_metrics']['backfoot']['img_4'],"backfoot_img4.jpg"),
        'backfoot_defense5': google_drive_url_to_image( document['drill_metrics']['backfoot']['img_5'],"backfoot_img5.jpg"),
        'backfoot_defense6': google_drive_url_to_image( document['drill_metrics']['backfoot']['img_6'],"backfoot_img6.jpg"),

        # POWER HITTING #
        'power_hitting_1': google_drive_url_to_image( document['drill_metrics']['power_hitting']['img_1'],"power_img1.jpg"),
        'power_hitting_2': google_drive_url_to_image( document['drill_metrics']['power_hitting']['img_2'],"power_img2.jpg"),
        'power_hitting_percentile': document['drill_metrics']['power_hitting']['percentile'],
        'power_hitting_rating': document['drill_metrics']['power_hitting']['grade'],
        'power_hitting_table' : table_data,
        'power_hitting_insights': document['drill_metrics']['power_hitting']['insights'],
        'power_hitting_improvements': document['drill_metrics']['power_hitting']['improvements'],

        # HOLD YOUR POSE 
        'hold_your_pose_1': google_drive_url_to_image( document['drill_metrics']['hold_your_pose']['img_1'],"hold_pose_1.png"),
        'hold_your_pose_1_shot_type': "Cover Drive",
        'hold_your_pose_1_duration':5,
        'hold_your_pose_2': google_drive_url_to_image( document['drill_metrics']['hold_your_pose']['img_2'],"hold_pose_2.png"),
        'hold_your_pose_2_shot_type': "Straight Drive",
        'hold_your_pose_2_duration': 4,
        'hold_your_pose_3':google_drive_url_to_image( document['drill_metrics']['hold_your_pose']['img_3'],"hold_pose_3.png"),
        'hold_your_pose_3_shot_type': "Straight Drive",
        'hold_your_pose_3_duration': 5,
        'hold_your_pose_4': google_drive_url_to_image( document['drill_metrics']['hold_your_pose']['img_4'],"hold_pose_4.png"),
        'hold_your_pose_4_shot_type': "Straight Drive",
        'hold_your_pose_4_duration': 5,
        'hold_your_pose_5': google_drive_url_to_image( document['drill_metrics']['hold_your_pose']['img_5'],"hold_pose_5.png"),
        'hold_your_pose_5_shot_type': "Cover Drive",
        'hold_your_pose_5_duration': 5,
        'hold_your_pose_6': google_drive_url_to_image( document['drill_metrics']['hold_your_pose']['img_6'],"hold_pose_6.png"),
        'hold_your_pose_6_shot_type': "Straight Drive",
        'hold_your_pose_6_duration': 5,
        'hold_your_pose_percentile': document['drill_metrics']['hold_your_pose']['percentile'],
        'hold_your_pose_rating': document['drill_metrics']['hold_your_pose']['grade'],
        'hold_your_pose_insights': document['drill_metrics']['hold_your_pose']['insights'],
        'hold_your_pose_improvements': document['drill_metrics']['hold_your_pose']['improvements'],
        
        'hold_your_pose_1_duration': hold_your_pose_ball_durations[0] if len(hold_your_pose_ball_durations) > 0 else None,
        'hold_your_pose_1_comment': hold_your_pose_ball_comments[0] if len(hold_your_pose_ball_comments) > 0 else None,
        'hold_your_pose_2_duration': hold_your_pose_ball_durations[1] if len(hold_your_pose_ball_durations) > 1 else None,
        'hold_your_pose_2_comment': hold_your_pose_ball_comments[1] if len(hold_your_pose_ball_comments) > 1 else None,
        'hold_your_pose_3_duration': hold_your_pose_ball_durations[2] if len(hold_your_pose_ball_durations) > 2 else None,
        'hold_your_pose_3_comment': hold_your_pose_ball_comments[2] if len(hold_your_pose_ball_comments) > 2 else None,
        'hold_your_pose_4_duration': hold_your_pose_ball_durations[3] if len(hold_your_pose_ball_durations) > 3 else None,
        'hold_your_pose_4_comment': hold_your_pose_ball_comments[3] if len(hold_your_pose_ball_comments) > 3 else None,
        'hold_your_pose_5_duration': hold_your_pose_ball_durations[4] if len(hold_your_pose_ball_durations) > 4 else None,
        'hold_your_pose_5_comment': hold_your_pose_ball_comments[4] if len(hold_your_pose_ball_comments) > 4 else None,
        'hold_your_pose_6_duration': hold_your_pose_ball_durations[5] if len(hold_your_pose_ball_durations) > 5 else None,
        'hold_your_pose_6_comment': hold_your_pose_ball_comments[5] if len(hold_your_pose_ball_comments) > 5 else None,


        # FEET PLANTED #
        'feet_planted_1': google_drive_url_to_image( document['drill_metrics']['feet_planted']['img_1'],"feet_planted_1.jpg"),
        'feet_planted_2': google_drive_url_to_image( document['drill_metrics']['feet_planted']['img_2'],"feet_planted_2.jpg"),
        'feet_planted_3': google_drive_url_to_image( document['drill_metrics']['feet_planted']['img_3'],"feet_planted_3.jpg"),
        'feet_planted_4': google_drive_url_to_image( document['drill_metrics']['feet_planted']['img_4'],"feet_planted_4.jpg"),
        'feet_planted_5': google_drive_url_to_image( document['drill_metrics']['feet_planted']['img_5'],"feet_planted_5.jpg"),
        'feet_planted_6': google_drive_url_to_image( document['drill_metrics']['feet_planted']['img_6'],"feet_planted_6.jpg"),
        'feet_planted_percentile': document['drill_metrics']['feet_planted']['percentile'],
        'feet_planted_rating': document['drill_metrics']['feet_planted']['grade'],
        # 'feet_planted_insights': document['drill_metrics']['feet_planted']['insights'],
        'feet_planted_improvements': document['drill_metrics']['feet_planted']['improvements'],
        
        'feet_planted_ball_1': document['drill_metrics']['feet_planted']['insights']['ball_comments'][0],
        'feet_planted_ball_1_comment': document['drill_metrics']['feet_planted']['insights']['ball_insights'][0],
        'feet_planted_ball_2': document['drill_metrics']['feet_planted']['insights']['ball_comments'][1],
        'feet_planted_ball_2_comment': document['drill_metrics']['feet_planted']['insights']['ball_insights'][1],
        'feet_planted_ball_3': document['drill_metrics']['feet_planted']['insights']['ball_comments'][2],
        'feet_planted_ball_3_comment': document['drill_metrics']['feet_planted']['insights']['ball_insights'][2],
        'feet_planted_ball_4': document['drill_metrics']['feet_planted']['insights']['ball_comments'][3],
        'feet_planted_ball_4_comment': document['drill_metrics']['feet_planted']['insights']['ball_insights'][3],
        'feet_planted_ball_5': document['drill_metrics']['feet_planted']['insights']['ball_comments'][4],
        'feet_planted_ball_5_comment': document['drill_metrics']['feet_planted']['insights']['ball_insights'][4],
        'feet_planted_ball_6': document['drill_metrics']['feet_planted']['insights']['ball_comments'][5],
        'feet_planted_ball_6_comment': document['drill_metrics']['feet_planted']['insights']['ball_insights'][5],

        # # RUNNING BETWEEN WICKETS #
        'running_bw_percentile': document['drill_metrics']['running_bw_wickets']['percentile'],
        'running_bw_rating':document['drill_metrics']['running_bw_wickets']['grade'],
        'run_time': document['drill_metrics']['running_bw_wickets']['run_time'],
        'avg_time': document['drill_metrics']['running_bw_wickets']['avg_time'],
        'running_bw_1': google_drive_url_to_image( document['drill_metrics']['running_bw_wickets']['img_1'],"running_1.jpg"),
        'running_bw_2': google_drive_url_to_image( document['drill_metrics']['running_bw_wickets']['img_2'],"running_2.jpg"),
        'running_bw_insights': document['drill_metrics']['running_bw_wickets']['insights'],
        'running_bw_improvements': document['drill_metrics']['running_bw_wickets']['improvements'],

    }

    output_path = generate_batting_drills_report(input_dict)
    return output_path