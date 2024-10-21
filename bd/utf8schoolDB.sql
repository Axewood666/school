--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: get_class_id_by_teacher(character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_class_id_by_teacher(t_first_name character varying, t_last_name character varying, t_middle_name character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    class_id INT;
BEGIN
    SELECT c.id INTO class_id
    FROM class c
    JOIN teacher t ON c.teacher_id = t.id
    WHERE t.first_name = t_first_name
      AND t.last_name = t_last_name
      AND t.middle_name = t_middle_name;
    
    RETURN class_id;
END;
$$;


ALTER FUNCTION public.get_class_id_by_teacher(t_first_name character varying, t_last_name character varying, t_middle_name character varying) OWNER TO postgres;

--
-- Name: get_class_id_by_teacher_name(character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_class_id_by_teacher_name(teacher_first_name character varying, teacher_last_name character varying, teacher_middle_name character varying DEFAULT NULL::character varying) RETURNS TABLE(classid integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT c.ClassID
    FROM Teacher t
    JOIN Class c ON t.TeacherID = c.TeacherID
    WHERE t.FirstName = teacher_first_name
      AND t.LastName = teacher_last_name
      AND (t.MiddleName = teacher_middle_name OR (teacher_middle_name IS NULL AND t.MiddleName IS NULL));
END;
$$;


ALTER FUNCTION public.get_class_id_by_teacher_name(teacher_first_name character varying, teacher_last_name character varying, teacher_middle_name character varying) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: class; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.class (
    classid integer NOT NULL,
    classname character varying(3) NOT NULL,
    teacherid integer,
    CONSTRAINT classname_regexp CHECK ((((classname)::text ~ '^[1-9][A-Z]$'::text) OR ((classname)::text ~ '^[1-9][0-1][A-Z]$'::text)))
);


ALTER TABLE public.class OWNER TO postgres;

--
-- Name: class_classid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.class_classid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.class_classid_seq OWNER TO postgres;

--
-- Name: class_classid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.class_classid_seq OWNED BY public.class.classid;


--
-- Name: grade; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.grade (
    gradeid integer NOT NULL,
    studentid integer NOT NULL,
    subjectid integer NOT NULL,
    date date NOT NULL,
    grade smallint,
    teacherid integer,
    CONSTRAINT grade_grade_check CHECK ((((grade)::numeric >= (0)::numeric) AND ((grade)::numeric <= (100)::numeric))),
    CONSTRAINT grades CHECK (((grade >= 1) AND (grade <= 5)))
);


ALTER TABLE public.grade OWNER TO postgres;

--
-- Name: grade_gradeid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.grade_gradeid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.grade_gradeid_seq OWNER TO postgres;

--
-- Name: grade_gradeid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.grade_gradeid_seq OWNED BY public.grade.gradeid;


--
-- Name: staff; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staff (
    staffid integer NOT NULL,
    firstname character varying(50) NOT NULL,
    middlename character varying(50),
    lastname character varying(50) NOT NULL,
    birthdate date NOT NULL,
    gender character(1),
    address character varying(255),
    phonenumber character varying(20),
    email character varying(100),
    CONSTRAINT staff_gender_check CHECK ((gender = ANY (ARRAY['M'::bpchar, 'F'::bpchar])))
);


ALTER TABLE public.staff OWNER TO postgres;

--
-- Name: staff_staffid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.staff_staffid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.staff_staffid_seq OWNER TO postgres;

--
-- Name: staff_staffid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.staff_staffid_seq OWNED BY public.staff.staffid;


--
-- Name: staffprofile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staffprofile (
    staffid integer NOT NULL,
    login character varying(255) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE public.staffprofile OWNER TO postgres;

--
-- Name: student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student (
    studentid integer NOT NULL,
    firstname character varying(50) NOT NULL,
    middlename character varying(50),
    lastname character varying(50) NOT NULL,
    birthdate date NOT NULL,
    gender character(1),
    address character varying(255),
    phonenumber character varying(20),
    email character varying(100),
    classid integer,
    CONSTRAINT student_gender_check CHECK ((gender = ANY (ARRAY['M'::bpchar, 'F'::bpchar])))
);


ALTER TABLE public.student OWNER TO postgres;

--
-- Name: student_studentid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.student_studentid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.student_studentid_seq OWNER TO postgres;

--
-- Name: student_studentid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.student_studentid_seq OWNED BY public.student.studentid;


--
-- Name: studentprofile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.studentprofile (
    studentid integer NOT NULL,
    login character varying(255) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE public.studentprofile OWNER TO postgres;

--
-- Name: subject; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subject (
    subjectid integer NOT NULL,
    subjectname character varying(100) NOT NULL
);


ALTER TABLE public.subject OWNER TO postgres;

--
-- Name: subject_subjectid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subject_subjectid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subject_subjectid_seq OWNER TO postgres;

--
-- Name: subject_subjectid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subject_subjectid_seq OWNED BY public.subject.subjectid;


--
-- Name: teacher; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teacher (
    teacherid integer NOT NULL,
    firstname character varying(50) NOT NULL,
    middlename character varying(50),
    lastname character varying(50) NOT NULL,
    birthdate date NOT NULL,
    gender character(1),
    address character varying(255),
    phonenumber character varying(20),
    email character varying(100),
    CONSTRAINT teacher_gender_check CHECK ((gender = ANY (ARRAY['M'::bpchar, 'F'::bpchar])))
);


ALTER TABLE public.teacher OWNER TO postgres;

--
-- Name: teacher_teacherid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.teacher_teacherid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.teacher_teacherid_seq OWNER TO postgres;

--
-- Name: teacher_teacherid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.teacher_teacherid_seq OWNED BY public.teacher.teacherid;


--
-- Name: teacherprofile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teacherprofile (
    teacherid integer NOT NULL,
    login character varying(255) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE public.teacherprofile OWNER TO postgres;

--
-- Name: teachersubject; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teachersubject (
    teacherid integer NOT NULL,
    subjectid integer NOT NULL
);


ALTER TABLE public.teachersubject OWNER TO postgres;

--
-- Name: class classid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class ALTER COLUMN classid SET DEFAULT nextval('public.class_classid_seq'::regclass);


--
-- Name: grade gradeid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grade ALTER COLUMN gradeid SET DEFAULT nextval('public.grade_gradeid_seq'::regclass);


--
-- Name: staff staffid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff ALTER COLUMN staffid SET DEFAULT nextval('public.staff_staffid_seq'::regclass);


--
-- Name: student studentid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student ALTER COLUMN studentid SET DEFAULT nextval('public.student_studentid_seq'::regclass);


--
-- Name: subject subjectid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject ALTER COLUMN subjectid SET DEFAULT nextval('public.subject_subjectid_seq'::regclass);


--
-- Name: teacher teacherid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher ALTER COLUMN teacherid SET DEFAULT nextval('public.teacher_teacherid_seq'::regclass);


--
-- Data for Name: class; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.class (classid, classname, teacherid) FROM stdin;
3	1A	5
4	1B	6
\.


--
-- Data for Name: grade; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.grade (gradeid, studentid, subjectid, date, grade, teacherid) FROM stdin;
39	7	10	2024-10-15	5	5
41	7	10	2024-10-15	1	5
42	7	10	2024-10-15	2	5
43	7	10	2024-10-15	4	5
44	7	10	2024-10-15	2	5
45	7	10	2024-10-15	2	5
46	7	10	2024-10-15	3	5
48	7	10	2024-10-15	1	5
57	7	10	2024-10-15	2	5
58	7	10	2024-10-15	2	5
59	7	10	2024-10-16	4	5
64	7	10	2024-10-16	3	5
65	7	10	2024-10-16	2	5
66	7	10	2024-10-16	3	5
67	7	10	2024-10-16	1	5
74	7	10	2024-10-18	2	5
76	9	10	2024-10-18	3	5
77	7	10	2024-10-18	3	5
78	7	10	2024-10-18	1	5
79	7	10	2024-10-18	3	5
80	7	10	2024-10-18	2	5
81	7	10	2024-10-18	2	5
82	7	10	2024-10-18	3	5
83	7	10	2024-10-18	2	5
84	8	10	2024-10-18	3	5
85	9	10	2024-10-18	2	5
87	9	10	2024-10-18	2	5
88	9	10	2024-10-18	3	5
89	7	10	2024-10-18	1	5
90	7	10	2024-10-18	2	5
91	7	10	2024-10-18	2	5
92	7	10	2024-10-18	1	5
93	7	10	2024-10-18	3	5
94	7	10	2024-10-18	2	5
95	7	10	2024-10-18	2	5
96	9	10	2024-10-18	5	5
97	8	10	2024-10-18	3	5
\.


--
-- Data for Name: staff; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.staff (staffid, firstname, middlename, lastname, birthdate, gender, address, phonenumber, email) FROM stdin;
1	╨Ш╨│╨╛╤А╤М	╨Ъ╨╛╨╜╤Б╤В╨░╨╜╤В╨╕╨╜╨╛╨▓╨╕╤З	╨Ц╤Г╨│╨░╤А	2004-03-07	M	╨╝╨╡╤А 6	8917934	igor@example.com
\.


--
-- Data for Name: staffprofile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.staffprofile (staffid, login, password) FROM stdin;
1	axewood	$1$SryDh9EW$FpOk/Ppc2L1UpETdAk9Kf/
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.student (studentid, firstname, middlename, lastname, birthdate, gender, address, phonenumber, email, classid) FROM stdin;
7	Alice	B.	Johnson	2005-04-10	F	789 Pine St, Springfield	555-0789	alicej@example.com	3
8	Bob	\N	Brown	2004-11-25	M	101 Maple St, Springfield	555-0678	bobb@example.com	4
9	Carol	C.	Davis	2005-07-23	F	202 Cedar St, Springfield	555-0567	carold@example.com	4
\.


--
-- Data for Name: studentprofile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.studentprofile (studentid, login, password) FROM stdin;
7	Alice	$1$lcEDSW4Q$xUsMonUkWWNIlafkfeVuI0
\.


--
-- Data for Name: subject; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subject (subjectid, subjectname) FROM stdin;
9	Mathematics
10	Science
11	History
12	Literature
\.


--
-- Data for Name: teacher; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teacher (teacherid, firstname, middlename, lastname, birthdate, gender, address, phonenumber, email) FROM stdin;
5	John	A.	Doe	1980-05-15	M	123 Elm St, Springfield	555-0123	johndoe@example.com
6	Jane	\N	Smith	1975-09-30	F	456 Oak St, Springfield	555-0456	janesmith@example.com
\.


--
-- Data for Name: teacherprofile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teacherprofile (teacherid, login, password) FROM stdin;
5	Jane	$1$mTIl45Fv$vWg7.nRuCEc3LFPEWrMZk/
\.


--
-- Data for Name: teachersubject; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teachersubject (teacherid, subjectid) FROM stdin;
5	9
5	10
6	11
6	12
\.


--
-- Name: class_classid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.class_classid_seq', 4, true);


--
-- Name: grade_gradeid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.grade_gradeid_seq', 97, true);


--
-- Name: staff_staffid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.staff_staffid_seq', 1, true);


--
-- Name: student_studentid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.student_studentid_seq', 9, true);


--
-- Name: subject_subjectid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subject_subjectid_seq', 12, true);


--
-- Name: teacher_teacherid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.teacher_teacherid_seq', 6, true);


--
-- Name: class class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class
    ADD CONSTRAINT class_pkey PRIMARY KEY (classid);


--
-- Name: grade grade_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grade
    ADD CONSTRAINT grade_pkey PRIMARY KEY (gradeid);


--
-- Name: staff staff_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_pkey PRIMARY KEY (staffid);


--
-- Name: staffprofile staffprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffprofile
    ADD CONSTRAINT staffprofile_pkey PRIMARY KEY (staffid);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (studentid);


--
-- Name: studentprofile studentprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studentprofile
    ADD CONSTRAINT studentprofile_pkey PRIMARY KEY (studentid);


--
-- Name: subject subject_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject
    ADD CONSTRAINT subject_pkey PRIMARY KEY (subjectid);


--
-- Name: teacher teacher_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher
    ADD CONSTRAINT teacher_pkey PRIMARY KEY (teacherid);


--
-- Name: teacherprofile teacherprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacherprofile
    ADD CONSTRAINT teacherprofile_pkey PRIMARY KEY (teacherid);


--
-- Name: teachersubject teachersubject_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teachersubject
    ADD CONSTRAINT teachersubject_pkey PRIMARY KEY (teacherid, subjectid);


--
-- Name: teacher unique_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher
    ADD CONSTRAINT unique_email UNIQUE (email);


--
-- Name: staff unique_staff_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT unique_staff_email UNIQUE (email);


--
-- Name: student unique_student_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT unique_student_email UNIQUE (email);


--
-- Name: class class_teacherid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class
    ADD CONSTRAINT class_teacherid_fkey FOREIGN KEY (teacherid) REFERENCES public.teacher(teacherid) ON DELETE SET NULL;


--
-- Name: staffprofile fk_staff; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffprofile
    ADD CONSTRAINT fk_staff FOREIGN KEY (staffid) REFERENCES public.staff(staffid);


--
-- Name: studentprofile fk_student; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studentprofile
    ADD CONSTRAINT fk_student FOREIGN KEY (studentid) REFERENCES public.student(studentid);


--
-- Name: teacherprofile fk_teacher; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacherprofile
    ADD CONSTRAINT fk_teacher FOREIGN KEY (teacherid) REFERENCES public.teacher(teacherid);


--
-- Name: grade grade_studentid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grade
    ADD CONSTRAINT grade_studentid_fkey FOREIGN KEY (studentid) REFERENCES public.student(studentid) ON DELETE CASCADE;


--
-- Name: grade grade_subjectid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grade
    ADD CONSTRAINT grade_subjectid_fkey FOREIGN KEY (subjectid) REFERENCES public.subject(subjectid) ON DELETE CASCADE;


--
-- Name: student student_classid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_classid_fkey FOREIGN KEY (classid) REFERENCES public.class(classid) ON DELETE SET NULL;


--
-- Name: grade teacher; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grade
    ADD CONSTRAINT teacher FOREIGN KEY (teacherid) REFERENCES public.teacher(teacherid);


--
-- Name: teachersubject teachersubject_subjectid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teachersubject
    ADD CONSTRAINT teachersubject_subjectid_fkey FOREIGN KEY (subjectid) REFERENCES public.subject(subjectid) ON DELETE CASCADE;


--
-- Name: teachersubject teachersubject_teacherid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teachersubject
    ADD CONSTRAINT teachersubject_teacherid_fkey FOREIGN KEY (teacherid) REFERENCES public.teacher(teacherid) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

