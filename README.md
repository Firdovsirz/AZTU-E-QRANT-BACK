## AzTU E-Qrant Back-End

Azərbaycan Texniki Universitetinin E-Qrant layihəsinin Back-End tərəfi.

## 👥 Layihədə iştirak edən şəxslər

Firdovsi Rzaev - Full-Stack Developer
Kərəm Şükürlü - Back-End Deloper

## Layihənin təsviri

Layihə Azərbaycan Texniki Universiteti üçün hazıranmışdır. Bu layihədə 2 hissədən ibarət olan girişdən istifadə olunur: Layihə rəhbəri və Layihə icraçısı.
Rəhbər olaraq giriş edilən zaman yeni layihələr əlavə etmək, layihədə görülən işlər, layihə işştirakçıları və layihə haqqında olan bütün məlumatlara nəzərət nəzərdə tutulub.
İcraşı olaraq giriş edilən zaman ilk öncə icraçının bütün çəlumatları tələb olunur. Növbəti addımda artıq icraçıya digər səhifələrə giriş icazəsi verilir. İcraçı istənilən layihədə iştirakçı ola bilir.
İştirakçı olduğu layihədə icraçının vəzifəsi layihədə görülən işlər, layihə haqqında məlumat (sərf olunan vaxt, layihənin smeta dəyəri və.s.) təmin etməlidir.

## ✅ Görülən işlər

- 👤 Firdovsi Rzaev
    - Qeydiyyat - Qeydiyyat zamanı istifadəçinin şifrəsinin Bcrypt ilə şifərlənməsi
        - Endpoint
            - /auth/signup - sistemdə qeydiyyat üçün
    - Daxil ol - İstifadəçinin Fin kod və şifrə ilə sistemə daxil olması nəzərdə tutulub.
        - Endpoint
            - /auth/signin - sistemə daxil olmaq üçün
    - Profil - İstifadəçinin şəxsi məlumatlarının verilənlər bazasında (PostgreSQL) - də saxlanılması
        və Front-End tərəfində istifadəsi üçün APİ
        - Endpoint
            - /api/profile/Fin_Kod - istifadəçinin şəxsi məlumatlarını görməyi üçün
            - /api/approve/profile - istifadəçinin profil məlumatlarını doldurması və profilini təsdiq etmək üçün
    - Util - tokenin yaradılması və dekodlaşdırılması (etibarlılıq müddətinin və digər məlumatların yoxlanılması)
        - JwtUtil
            - encode_auth_token funksiyası - tokenin yaradılması və özündə məlumatların saxlaması üçün
            - decode_auth_token funksiyası - tokenin dekodlaşdırılması və yoxlanılması