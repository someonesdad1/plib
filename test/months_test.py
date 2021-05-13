from months import months
from lwtest import run

def Test():
    assert months[1] == "Jan"
    assert months[2] == "Feb"
    assert months[3] == "Mar"
    assert months[4] == "Apr"
    assert months[5] == "May"
    assert months[6] == "Jun"
    assert months[7] == "Jul"
    assert months[8] == "Aug"
    assert months[9] == "Sep"
    assert months[10] == "Oct"
    assert months[11] == "Nov"
    assert months[12] == "Dec"
    #
    assert months("Jan") == 1
    assert months("Feb") == 2
    assert months("Mar") == 3
    assert months("Apr") == 4
    assert months("May") == 5
    assert months("Jun") == 6
    assert months("Jul") == 7
    assert months("Aug") == 8
    assert months("Sep") == 9
    assert months("Oct") == 10
    assert months("Nov") == 11
    assert months("Dec") == 12

if __name__ == "__main__":
    exit(run(globals())[0])
