PGDMP     '    !                |            Social    15.4    15.4 B    M           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            N           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            O           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            P           1262    57503    Social    DATABASE     �   CREATE DATABASE "Social" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Kazakhstan.1252';
    DROP DATABASE "Social";
                postgres    false            �            1259    57533    comments    TABLE     �   CREATE TABLE public.comments (
    comment_id integer NOT NULL,
    post_id integer,
    user_id integer,
    content text NOT NULL,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.comments;
       public         heap    postgres    false            �            1259    57532    comments_comment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.comments_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.comments_comment_id_seq;
       public          postgres    false    219            Q           0    0    comments_comment_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.comments_comment_id_seq OWNED BY public.comments.comment_id;
          public          postgres    false    218            �            1259    65855    friends    TABLE     �  CREATE TABLE public.friends (
    id integer NOT NULL,
    user_id1 integer,
    user_id2 integer,
    status character varying(50) DEFAULT 'pending'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT friends_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'accepted'::character varying, 'rejected'::character varying])::text[])))
);
    DROP TABLE public.friends;
       public         heap    postgres    false            �            1259    65854    friends_id_seq    SEQUENCE     �   CREATE SEQUENCE public.friends_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.friends_id_seq;
       public          postgres    false    227            R           0    0    friends_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.friends_id_seq OWNED BY public.friends.id;
          public          postgres    false    226            �            1259    57553    likes    TABLE     �   CREATE TABLE public.likes (
    like_id integer NOT NULL,
    post_id integer,
    comment_id integer,
    user_id integer,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.likes;
       public         heap    postgres    false            �            1259    57552    likes_like_id_seq    SEQUENCE     �   CREATE SEQUENCE public.likes_like_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.likes_like_id_seq;
       public          postgres    false    221            S           0    0    likes_like_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.likes_like_id_seq OWNED BY public.likes.like_id;
          public          postgres    false    220            �            1259    57576    messages    TABLE     �   CREATE TABLE public.messages (
    message_id integer NOT NULL,
    sender_id integer,
    receiver_id integer,
    content text NOT NULL,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.messages;
       public         heap    postgres    false            �            1259    57575    messages_message_id_seq    SEQUENCE     �   CREATE SEQUENCE public.messages_message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.messages_message_id_seq;
       public          postgres    false    223            T           0    0    messages_message_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.messages_message_id_seq OWNED BY public.messages.message_id;
          public          postgres    false    222            �            1259    57596    notifications    TABLE     �   CREATE TABLE public.notifications (
    notification_id integer NOT NULL,
    user_id integer,
    content text NOT NULL,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(50)
);
 !   DROP TABLE public.notifications;
       public         heap    postgres    false            �            1259    57595 !   notifications_notification_id_seq    SEQUENCE     �   CREATE SEQUENCE public.notifications_notification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.notifications_notification_id_seq;
       public          postgres    false    225            U           0    0 !   notifications_notification_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.notifications_notification_id_seq OWNED BY public.notifications.notification_id;
          public          postgres    false    224            �            1259    57518    posts    TABLE     �   CREATE TABLE public.posts (
    post_id integer NOT NULL,
    user_id integer,
    content text NOT NULL,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.posts;
       public         heap    postgres    false            �            1259    57517    posts_post_id_seq    SEQUENCE     �   CREATE SEQUENCE public.posts_post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.posts_post_id_seq;
       public          postgres    false    217            V           0    0    posts_post_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.posts_post_id_seq OWNED BY public.posts.post_id;
          public          postgres    false    216            �            1259    57505    users    TABLE     n  CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    f_name character varying(255) NOT NULL,
    s_name character varying(255) NOT NULL,
    dob date NOT NULL,
    phone character varying(15) NOT NULL,
    picture text
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    57504    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public          postgres    false    215            W           0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public          postgres    false    214            �           2604    57536    comments comment_id    DEFAULT     z   ALTER TABLE ONLY public.comments ALTER COLUMN comment_id SET DEFAULT nextval('public.comments_comment_id_seq'::regclass);
 B   ALTER TABLE public.comments ALTER COLUMN comment_id DROP DEFAULT;
       public          postgres    false    218    219    219            �           2604    65858 
   friends id    DEFAULT     h   ALTER TABLE ONLY public.friends ALTER COLUMN id SET DEFAULT nextval('public.friends_id_seq'::regclass);
 9   ALTER TABLE public.friends ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    227    226    227            �           2604    57556    likes like_id    DEFAULT     n   ALTER TABLE ONLY public.likes ALTER COLUMN like_id SET DEFAULT nextval('public.likes_like_id_seq'::regclass);
 <   ALTER TABLE public.likes ALTER COLUMN like_id DROP DEFAULT;
       public          postgres    false    220    221    221            �           2604    57579    messages message_id    DEFAULT     z   ALTER TABLE ONLY public.messages ALTER COLUMN message_id SET DEFAULT nextval('public.messages_message_id_seq'::regclass);
 B   ALTER TABLE public.messages ALTER COLUMN message_id DROP DEFAULT;
       public          postgres    false    222    223    223            �           2604    57599    notifications notification_id    DEFAULT     �   ALTER TABLE ONLY public.notifications ALTER COLUMN notification_id SET DEFAULT nextval('public.notifications_notification_id_seq'::regclass);
 L   ALTER TABLE public.notifications ALTER COLUMN notification_id DROP DEFAULT;
       public          postgres    false    225    224    225            �           2604    57521    posts post_id    DEFAULT     n   ALTER TABLE ONLY public.posts ALTER COLUMN post_id SET DEFAULT nextval('public.posts_post_id_seq'::regclass);
 <   ALTER TABLE public.posts ALTER COLUMN post_id DROP DEFAULT;
       public          postgres    false    217    216    217            �           2604    57508    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public          postgres    false    215    214    215            B          0    57533    comments 
   TABLE DATA           V   COPY public.comments (comment_id, post_id, user_id, content, "timestamp") FROM stdin;
    public          postgres    false    219   QO       J          0    65855    friends 
   TABLE DATA           M   COPY public.friends (id, user_id1, user_id2, status, created_at) FROM stdin;
    public          postgres    false    227   nO       D          0    57553    likes 
   TABLE DATA           S   COPY public.likes (like_id, post_id, comment_id, user_id, "timestamp") FROM stdin;
    public          postgres    false    221   �O       F          0    57576    messages 
   TABLE DATA           \   COPY public.messages (message_id, sender_id, receiver_id, content, "timestamp") FROM stdin;
    public          postgres    false    223   �O       H          0    57596    notifications 
   TABLE DATA           _   COPY public.notifications (notification_id, user_id, content, "timestamp", status) FROM stdin;
    public          postgres    false    225   P       @          0    57518    posts 
   TABLE DATA           G   COPY public.posts (post_id, user_id, content, "timestamp") FROM stdin;
    public          postgres    false    217   P       >          0    57505    users 
   TABLE DATA           h   COPY public.users (user_id, username, password, email, f_name, s_name, dob, phone, picture) FROM stdin;
    public          postgres    false    215   <P       X           0    0    comments_comment_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.comments_comment_id_seq', 1, false);
          public          postgres    false    218            Y           0    0    friends_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.friends_id_seq', 4, true);
          public          postgres    false    226            Z           0    0    likes_like_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.likes_like_id_seq', 1, false);
          public          postgres    false    220            [           0    0    messages_message_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.messages_message_id_seq', 1, false);
          public          postgres    false    222            \           0    0 !   notifications_notification_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.notifications_notification_id_seq', 1, false);
          public          postgres    false    224            ]           0    0    posts_post_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.posts_post_id_seq', 1, false);
          public          postgres    false    216            ^           0    0    users_user_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.users_user_id_seq', 13, true);
          public          postgres    false    214            �           2606    57541    comments comments_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (comment_id);
 @   ALTER TABLE ONLY public.comments DROP CONSTRAINT comments_pkey;
       public            postgres    false    219            �           2606    65863    friends friends_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.friends
    ADD CONSTRAINT friends_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.friends DROP CONSTRAINT friends_pkey;
       public            postgres    false    227            �           2606    57559    likes likes_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_pkey PRIMARY KEY (like_id);
 :   ALTER TABLE ONLY public.likes DROP CONSTRAINT likes_pkey;
       public            postgres    false    221            �           2606    57584    messages messages_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (message_id);
 @   ALTER TABLE ONLY public.messages DROP CONSTRAINT messages_pkey;
       public            postgres    false    223            �           2606    57604     notifications notifications_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (notification_id);
 J   ALTER TABLE ONLY public.notifications DROP CONSTRAINT notifications_pkey;
       public            postgres    false    225            �           2606    57526    posts posts_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (post_id);
 :   ALTER TABLE ONLY public.posts DROP CONSTRAINT posts_pkey;
       public            postgres    false    217            �           2606    57516    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public            postgres    false    215            �           2606    57512    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    215            �           2606    57514    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public            postgres    false    215            �           2606    57542    comments comments_post_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(post_id);
 H   ALTER TABLE ONLY public.comments DROP CONSTRAINT comments_post_id_fkey;
       public          postgres    false    219    3225    217            �           2606    57547    comments comments_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);
 H   ALTER TABLE ONLY public.comments DROP CONSTRAINT comments_user_id_fkey;
       public          postgres    false    219    215    3221            �           2606    65864    friends friends_user_id1_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.friends
    ADD CONSTRAINT friends_user_id1_fkey FOREIGN KEY (user_id1) REFERENCES public.users(user_id);
 G   ALTER TABLE ONLY public.friends DROP CONSTRAINT friends_user_id1_fkey;
       public          postgres    false    227    3221    215            �           2606    65869    friends friends_user_id2_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.friends
    ADD CONSTRAINT friends_user_id2_fkey FOREIGN KEY (user_id2) REFERENCES public.users(user_id);
 G   ALTER TABLE ONLY public.friends DROP CONSTRAINT friends_user_id2_fkey;
       public          postgres    false    215    3221    227            �           2606    57565    likes likes_comment_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_comment_id_fkey FOREIGN KEY (comment_id) REFERENCES public.comments(comment_id);
 E   ALTER TABLE ONLY public.likes DROP CONSTRAINT likes_comment_id_fkey;
       public          postgres    false    219    3227    221            �           2606    57560    likes likes_post_id_fkey    FK CONSTRAINT     |   ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(post_id);
 B   ALTER TABLE ONLY public.likes DROP CONSTRAINT likes_post_id_fkey;
       public          postgres    false    217    3225    221            �           2606    57570    likes likes_user_id_fkey    FK CONSTRAINT     |   ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);
 B   ALTER TABLE ONLY public.likes DROP CONSTRAINT likes_user_id_fkey;
       public          postgres    false    215    3221    221            �           2606    57590 "   messages messages_receiver_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_receiver_id_fkey FOREIGN KEY (receiver_id) REFERENCES public.users(user_id);
 L   ALTER TABLE ONLY public.messages DROP CONSTRAINT messages_receiver_id_fkey;
       public          postgres    false    215    223    3221            �           2606    57585     messages messages_sender_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(user_id);
 J   ALTER TABLE ONLY public.messages DROP CONSTRAINT messages_sender_id_fkey;
       public          postgres    false    215    3221    223            �           2606    57605 (   notifications notifications_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);
 R   ALTER TABLE ONLY public.notifications DROP CONSTRAINT notifications_user_id_fkey;
       public          postgres    false    3221    225    215            �           2606    57527    posts posts_user_id_fkey    FK CONSTRAINT     |   ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);
 B   ALTER TABLE ONLY public.posts DROP CONSTRAINT posts_user_id_fkey;
       public          postgres    false    215    3221    217            B      x������ � �      J   J   x�3�4�4�LLNN-(IM�4202�50�52V02�2��25�376650�2�4#J�1P�Q*M�*-�R���� �%      D      x������ � �      F      x������ � �      H      x������ � �      @      x������ � �      >   M  x�m�=o� �����V�6l:�j�v�ј&�,c�U~}�H"�����{�3�ū	�(��vS�����ڨi�AU;g�1��)�B���Ť��i�@нMB�+��QZUy���-,��5������#H�a�&'@�F������%�A�n�F�!�b2n�PP��
��eH`�01���Ik:nR����<��L{m�է��R��b���MR�Ҧ~��r�]>Y鏜:ۢ�&�ukL��M(�%&e�ት�����"ޢx�� n�.��d�.��m�'����.xW�q�����;�K�R��S)|u�������*���M�     