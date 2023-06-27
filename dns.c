#include <stdio.h>

#define MAXQUESTION 100

/* Structure definitions */
struct DNSHeader {
    int id;
    int flags;
    int num_questions;    // = 0
    int num_answers;      // = 0
    int num_authorities;  // = 0
    int num_additionals;  // = 0
};

struct DNSQuestion {
    int name[];
    int type;
    int class;
};

/* Function declarations */
struct DNSHeader make_header(int id, int flags, int num_questions, int num_answers, int num_authorities, int num_additionals);

struct DNSQuestion make_question(int name[], int type, int class, int lim);

int main()
{

    struct DNSHeader header;
    struct DNSQuestion question;

    header = make_header(5, 10, 1, 2, 3, 4);
    question = make_question("google", 5, 10, MAXQUESTION);

    printf("Header.id: %d\n", header.id);
    printf("Question.type: %d\n", question.type);

    return 0;
}


/* Make DNS header from query components */
struct DNSHeader make_header(int id, int flags, int num_questions, int num_answers, int num_authorities, int num_additionals)
{
    struct DNSHeader header;

    header.id               = id;
    header.flags            = flags;
    header.num_questions    = num_questions   ? num_questions   : 0;
    header.num_answers      = num_answers     ? num_answers     : 0;
    header.num_authorities  = num_authorities ? num_authorities : 0;
    header.num_additionals  = num_additionals ? num_additionals : 0;

    return header;
}

/* Make DNS question */
struct DNSQuestion make_question(int name[], int type, int class, int lim)
{
    struct DNSQuestion question;

    question.name  = name[];
    question.type  = type;
    question.class = class;
}
